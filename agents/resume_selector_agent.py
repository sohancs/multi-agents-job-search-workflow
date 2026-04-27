
from langchain_openai import ChatOpenAI
from configs import OPENAI_MODEL, OPENAI_API_KEY
from state import AgentState

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, temperature=0.1)

def resume_selector(state : AgentState) :
    """Select the most relevant resume for given job description using LLM."""

    resumes = ["AI", "Backend"]
    
    filtered_jobs = state.get("filtered_jobs", [])

    for job in filtered_jobs:
        prompt = f"""Given job description/ title, " \
        "Job description : {job['title']}" \
        "select the most relevant resume and return only one word from below options:" \
        "AI, Backend, NONE"""

        result =llm.invoke(prompt).content.strip()
        job["selected_resume"] = result if result in resumes else "Backend"

    return state
