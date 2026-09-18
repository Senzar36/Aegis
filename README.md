# 🛡️ AEGIS — Unified Student Dashboard

## 🔍 Why this project exists
Students constantly switch between multiple tools — email, timetable, notes, and reminders — leading to inefficiency and missed information. AEGIS was built to unify all essential academic workflows into a single, integrated system.

## 🚀 What it does
AEGIS is a centralized dashboard that:
- Syncs emails
- Displays timetable from structured data
- Stores notes and attachments
- Manages reminders

All within a single interface.

## 🧠 Key Idea
Instead of building separate tools, AEGIS integrates multiple student utilities into one backend-driven system using structured data and automation.

## ✨ What makes it different
- Combines **email + timetable + notes + reminders**
- Uses **structured Excel ingestion for schedules**
- Backend-driven architecture (not just frontend UI)

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

6. **IMPORTANT THINGS FOR THE PROGRAM TO WORK**
This program is in very basic form and can be used for personal use.
In order to run the program, make sure the files are in the same order as the structure provided.
