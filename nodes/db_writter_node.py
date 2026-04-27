from state import AgentState
import sqlite3
from datetime import datetime 

def db_writter_fn(state : AgentState) -> dict:
    """Write the relevant job details to database."""
    reranked_jobs =state.get("reranked_jobs", [])
    conn = sqlite3.connect('db/jobs.db')
    cursor = conn.cursor()

    if not reranked_jobs:
        print("No jobs to write in database")
        return {}
    

    for job in reranked_jobs:
        try:
            job_dtls = job.job_dtls
            
            cursor.execute("""
                INSERT OR IGNORE INTO filtered_jobs (
                    date_scraped, company_name, job_title, source, job_description, job_link, location, recruiter_name, recruiter_email, resume_used, match_score, status, notes, matching_skills
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           job_dtls.get("companyName",""),
                           job_dtls.get("title",""),
                           job_dtls.get("_source",""),
                           job_dtls.get("descriptionText",""),
                           job_dtls.get("link",""),
                           job_dtls.get("location",""),
                           job_dtls.get("jobPosterName",""),
                           job_dtls.get("recruiter_email",""),
                           job_dtls.get("selected_resume",""),
                           job.relevance_score,
                           "NEW",
                           job.reasoning,
                           ",".join(job.matching_skills)
                        )
            )
        except sqlite3.Error as e:
            print(f"Error occurred while writing to database: {e}")
            conn.rollback()
            conn.close()

    conn.commit()
    conn.close()
    print(f"{len(reranked_jobs)} jobs written to db successfully.")

    return {}

def update_job_status(state : AgentState) :
    "Update job status for drafted emails"
    conn = sqlite3.connect('db/jobs.db')
    cursor = conn.cursor()

    mail_drafts = state.get("mail_drafts", [])

    for job in mail_drafts :
        status = job.get("email_draft_response", "")
        job_dtls = job.get("job_dtls", {})

        cursor.execute("UPDATE filtered_jobs SET STATUS = ? WHERE JOB_LINK = ?",(str(status).upper(), job_dtls["link"]))

    conn.commit()
    conn.close()

    return {}