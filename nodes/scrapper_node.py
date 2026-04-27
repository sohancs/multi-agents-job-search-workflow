from state import AgentState
from tools.scrapper_tools import linkedin_job_scrapper

def scrap_jobs(state : AgentState) -> dict:
    """Scrap jobs from multiple job portals and update the state."""
    job_listings = linkedin_job_scrapper.invoke({})

    print(f"Scrapped {len(job_listings)} job listings from LinkedIn")

    if not job_listings or (len(job_listings) > 0  and "_error" in job_listings[0]):
        state["raw_jobs"] = []
        print(f"Error in scrapping jobs from source {job_listings[0]['_source']} - {job_listings[0]['_error']}")
    else:    
        state["raw_jobs"] = job_listings

    return {"raw_jobs" : state["raw_jobs"]}

    