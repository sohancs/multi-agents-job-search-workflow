from db.init_db import init_db_fn
from job_workflow import build_workflow
from nodes.load_resume_node import resume_loader
from state import AgentState
from datetime import datetime

def main_fn():
    """Initialize the database and execute the job search workflow."""

    job_started_at = datetime.now()
    print(f"Workflow started at {job_started_at}.")
    
    init_db_fn()

    resumes = resume_loader() #preload the resume before starting of workflow
    
    workflow = build_workflow()
    
    initial_state = {
        "raw_jobs": [],
        "filtered_jobs": [],
        "resumes": resumes,
        "ranked_jobs": [],
        "mail_drafts": []
    }
    
    result = workflow.invoke(initial_state)

    print(f"Workflow completed in {datetime.now() - job_started_at}.")

if __name__ == "__main__":
    main_fn()