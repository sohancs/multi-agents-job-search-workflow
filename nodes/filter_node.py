from state import AgentState


def filter_jobs(state : AgentState) -> dict:
    """Filter the raw jobs which are duplicated"""
    raw_jobs = state.get("raw_jobs",[])

    if not raw_jobs:
        print("No jobs to filter")
        state["filtered_jobs"] = []
        return
    
    seen_jobs = set()
    filtered_job_list : list = []


    for job in raw_jobs:
        link = job.get("link")
        if link and link not in seen_jobs:
            seen_jobs.add(link)
            filtered_job_list.append(job)

    print("Number of unique jobs after filering : ", len(filtered_job_list))

    return {"filtered_jobs" : filtered_job_list}