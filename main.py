import os
import shutil
import psutil
import time
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from mail_engine import sync_emails
from database import get_db

app = FastAPI()

print(f"DEBUG: Looking for static files in: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')}")
print(f"DEBUG: Does index.html exist there? {os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'index.html'))}")

# Setup paths
base_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(base_dir, "static")
storage_path = os.path.join(base_dir, "storage")
excel_path = os.path.join(base_dir, "timetable.xlsx")

if not os.path.exists(storage_path):
    os.makedirs(storage_path)

# Helper for Excel Time Formatting
def format_excel_time(t):
    try:
        if pd.isna(t): return "00:00"
        time_str = str(t)
        if " " in time_str:
            time_str = time_str.split(" ")[1]
        return time_str[:5]
    except:
        return "00:00"

# --- SYSTEM HEALTH ---
@app.get("/system-status")
def get_system_status():
    disk = psutil.disk_usage('/')
    battery = psutil.sensors_battery()
    return {
        "disk_free": f"{disk.free / (1024**3):.2f} GB",
        "disk_percent": disk.percent,
        "battery_percent": battery.percent if battery else "N/A",
        "is_plugged": battery.power_plugged if battery else False,
        "ram_percent": psutil.virtual_memory().percent
    }

# --- EMAIL MODULE ---
@app.get("/sync")
def trigger_sync():
    sync_emails()
    return {"message": "Sync complete"}

@app.get("/emails")
def get_emails():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM emails ORDER BY received_at DESC")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

# --- NOTES MODULE ---
@app.post("/add-note")
async def add_note(title: str = Form(...), content: str = Form(...), file: UploadFile = File(None)):
    db = get_db()
    cursor = db.cursor()
    file_rel_path = None
    if file:
        file_path = os.path.join(storage_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_rel_path = f"storage/{file.filename}"
    cursor.execute("INSERT INTO notes (title, content, file_path) VALUES (%s, %s, %s)", (title, content, file_rel_path))
    db.commit()
    cursor.close()
    db.close()
    return {"status": "success"}

@app.get("/notes")
def get_notes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

# --- CALENDAR MODULE ---
@app.post("/add-reminder")
async def add_reminder(title: str = Form(...), remind_date: str = Form(...), category: str = Form(...)):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO reminders (title, remind_date, category) VALUES (%s, %s, %s)", (title, remind_date, category))
    db.commit()
    cursor.close()
    db.close()
    return {"status": "success"}

@app.get("/reminders")
def get_reminders():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reminders WHERE remind_date >= CURDATE() ORDER BY remind_date ASC")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

# --- TIMETABLE MODULE ---
@app.get("/sync-timetable")
def sync_local_timetable():
    if not os.path.exists(excel_path):
        return {"error": "timetable.xlsx not found."}
    try:
        df = pd.read_excel(excel_path, engine='openpyxl').dropna(how='all')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM timetable")
        count = 0
        for _, row in df.iterrows():
            if pd.isna(row['Day']) or pd.isna(row['Subject']): continue
            start = format_excel_time(row['Start'])
            end = format_excel_time(row['End'])
            query = "INSERT INTO timetable (day_of_week, subject_name, start_time, end_time, room_number) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (str(row['Day']).strip(), str(row['Subject']).strip(), start, end, str(row['Room']).strip()))
            count += 1
        db.commit()
        cursor.close()
        db.close()
        return {"status": "success", "rows_synced": count}
    except Exception as e:
        return {"error": str(e)}

@app.get("/timetable")
def get_timetable():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM timetable ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), start_time ASC"
    cursor.execute(query)
    data = cursor.fetchall()
    for item in data:
        item['start_time'] = str(item['start_time'])[:5]
        item['end_time'] = str(item['end_time'])[:5]
    cursor.close()
    db.close()
    return data

@app.get("/")
async def read_index():
    # Adding a timestamp query forces the browser to think it's a new request
    return FileResponse(os.path.join(static_path, "index.html"), headers={"Cache-Control": "no-store"})

app.mount("/storage", StaticFiles(directory=storage_path), name="storage")
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)