from langchain_openai import ChatOpenAI
from configs import OPENAI_MODEL, OPENAI_API_KEY
from state import AgentState
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, temperature=0.1)

class JobMatchResult(BaseModel):
    relevance_score: int = 0
    matching_skills: list[str] = []
    missing_skills: list[str] = []
    reasoning: str = ""
    job_dtls: dict = {}


parser = PydanticOutputParser(pydantic_object=JobMatchResult)

def rerank_jobs(state : AgentState) -> dict :
    """Rerank the filtered jobs based on relevance based on resumes using LLM."""

    filtered_jobs = state.get("filtered_jobs",[])
    resumes = state.get("resumes", {})

    final_ranked_jobs : list[JobMatchResult] = []
    for job in filtered_jobs:
        try:
            prompt = f"""You are Senior recruiter who assess 1000 of resumes per day. Now you have task to assess below job description and resume
            and return output in below format :
            Inputs:
            Job Title : {job['title']}
            Company : {job['companyName']}
            Job Description : {job['descriptionText'] or job['description']}

            Resume : {resumes.get(job.get("selected_resume", ""))}

            Output: 
            {{
                "relevance_score" : <1-10> - where 1 is least relevant and 10 is most relevant,
                "matching_skills" : <required matching skills between job description and resume>
                "missing_skills" : <required skills required for job that are missing in resume>,
                "reasoning" : <brief reasoning for the given relevance score>
            }}"""

            result = llm.invoke(prompt).content.strip()

            #create custom dict to hold job details and llm output together
            parsed_obj = parser.parse(result)
            parsed_obj.job_dtls = job

            final_ranked_jobs.append(parsed_obj)
        except Exception as ex:
            print(f"Error in reranking agent for job {job.get('title','')} at {job.get('companyName','')} - {ex}")
        
    #sort the jobs based on relevance score in descending order    
    final_ranked_jobs.sort(key=lambda x: x.relevance_score, reverse=True)

    #filter out jobs with relevance score less than 6
    final_ranked_jobs = [job for job in final_ranked_jobs if job.relevance_score >= 6]


    return {"reranked_jobs" : final_ranked_jobs}