from typing import Dict
from typing import TypedDict

class AgentState(TypedDict):
    raw_jobs : list
    filtered_jobs : list
    resumes: dict
    reranked_jobs: list
    mail_drafts: list
