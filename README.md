**AEGIS: PROJECT OVERVIEW**
**PROJECT NAME**: AEGIS (Advanced Integrated System)
**PURPOSE**: Unified College Administrative Dashboard
**CORE STACK**: Python (FastAPI), MySQL, JavaScript (ES6), CSS3, Pandas

1. **DIRECTORY STRUCTURE**
Aegis/
├── main.py              (Backend API & Server Logic)
├── database.py          (MySQL Connection Configuration)
├── mail_engine.py       (Gmail API Sync Logic)
├── timetable.xlsx       (Source Excel file for schedule)
├── storage/             (Upload directory for note attachments)
└── static/
└── index.html       (Frontend UI & JavaScript Logic)

2. **DATABASE SCHEMA (SQL)**
Execute these commands in MySQL Workbench to prepare the environment:

CREATE DATABASE aegis;
USE aegis;

CREATE TABLE timetable (id INT AUTO_INCREMENT PRIMARY KEY, day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), subject_name VARCHAR(255), start_time TIME, end_time TIME, room_number VARCHAR(50));

CREATE TABLE emails (id INT AUTO_INCREMENT PRIMARY KEY, sender VARCHAR(255), subject VARCHAR(255), body TEXT, received_at DATETIME);

CREATE TABLE notes (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), content TEXT, file_path VARCHAR(500), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE reminders (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), remind_date DATE, category VARCHAR(50));

3. **EXCEL FILE FORMAT (TIMETABLE.XLSX)**
The Excel file must have exactly 5 columns with these headers:
[Day] | [Subject] | [Start] | [End] | [Room]

IMPORTANT: Every row must have the Day written out (e.g., "Monday"). Do not use merged cells.

Make multiple rows of the same day to display multiple classes in the Timetable.

TIME FORMAT: Use 24-hour format (e.g., 09:00, 13:30).

4. **INSTALLATION COMMANDS**
Open your terminal in the project folder and run:
pip install fastapi uvicorn pandas openpyxl mysql-connector-python psutil

5. **RUNNING THE SYSTEM**
Start the MySQL server.

Open the terminal in the Aegis folder.

Run: python main.py

Open your browser to: http://localhost:8000