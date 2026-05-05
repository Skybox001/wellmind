# WellMind (Mental Health Support AI)

## Requirements
- Python 3.x
- MySQL Server running on `localhost` (default port `3306`)

## Setup
### 1) Create a virtual environment + install dependencies (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2) Configure environment variables
- Copy `.env.example` to `.env` and fill in values:
  - `FLASK_SECRET_KEY`
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

### 3) Create the database/table (one-time)
Run in a MySQL client:
```sql
CREATE DATABASE IF NOT EXISTS chatbot;
USE chatbot;
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);
```

## Run
```powershell
.\.venv\Scripts\python.exe run_project.py
```

Open: http://127.0.0.1:5000

## Predefined user login (if present in your DB)
- Username: `admin`
- Password: `123456`
