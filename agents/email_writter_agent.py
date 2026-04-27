
from langchain_openai import ChatOpenAI
from configs import OPENAI_MODEL, OPENAI_API_KEY, CANDIDATE_NAME, CANDIDATE_GITHUB_URL, CANDIDATE_LINKEDIN_URL, CANDIDATE_MOB_NO
from state import AgentState
import json

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, temperature=0.1)

def write_email_agent_fn(state: AgentState) :
    """Agent responsible to write email based on Job description and resume."""
    reranked_jobs =state.get("reranked_jobs", [])
    resumes = state.get("resumes", {})

    mail_drafts = []

    if not reranked_jobs:
        print("No jobs to write in database")
        return {}


    for job in reranked_jobs:
        job_details = job.job_dtls
        prompt = f"""You are professional email writer & HR recruiter. Given the job description and selected resume, draft a personalized email to the recruiter.
                    Subject line: concise, mentions role, experience and notice period as 1 month in this format <JD Title | Years of Experience | Notice period>
                    Email body: 1. It should be short and concise, only relevent skills sets, make 2 paraghraghs :
                                        i. Brief introduction of candidate with relevant experience and skills, current working company<take current company from given resume> and overall years of experience. 
                                        ii. Highlight key matching skills and experience based on job description. 
                                3. Polite closing statement in 1 sentence.
                                4.email signature with name, mobile_no - {"Mob :" + CANDIDATE_MOB_NO}, linkedIn url - {"LinkedIn :" + CANDIDATE_LINKEDIN_URL} & github url - {"GitHub :" + CANDIDATE_GITHUB_URL} in seperate lines.
                                (Important: Provide only the raw URL inside the href attribute, no Markdown []() syntax.)
                    Sound human, not corporate or AI generated.

                    and return output in below format :
                    Inputs:
                    CANDIDATE NAME : {CANDIDATE_NAME}
                    Job Title : {job_details['title']}
                    Company : {job_details['companyName']}
                    Job Description : {job_details['descriptionText'] or job_details['description']}

                    Resume : {resumes.get(job_details.get("selected_resume", ""))}

                    Output: 
                    {{
                        "subject" : <email subject line>,
                        "body" : <email body>,
                        "recruiter_email" : <recruiter email extracted from job_details if available else empty string>
                    }}"""
        
        result = llm.invoke(prompt).content.strip()
        parse_result = json.loads(result)
        parse_result["job_dtls"] = job_details

        mail_drafts.append(parse_result)
        
    return {"mail_drafts" : mail_drafts}

