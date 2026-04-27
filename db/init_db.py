import sqlite3

def init_db_fn():
    conn = sqlite3.connect('db/jobs.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filtered_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_scraped TEXT,
        company_name TEXT,
        job_title TEXT,
        source TEXT,
        job_description TEXT,
        job_link TEXT UNIQUE,
        location TEXT,
        recruiter_name TEXT,
        recruiter_email TEXT,
        resume_used TEXT,
        match_score INTEGER,
        status TEXT,
        notes TEXT,
        matching_skills TEXT
        )
   """)
    
    conn.commit()
    conn.close()