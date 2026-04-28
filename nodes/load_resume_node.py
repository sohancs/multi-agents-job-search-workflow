from state import AgentState
from langchain_community.document_loaders import PyPDFLoader

def resume_loader() -> dict:
    """Load the resume content on workflow startup."""

    resumes = {}

    files = {
        "AI" : "resumes/Sohan-Chitte-GenAI-Resume.pdf",
        "Backend": "resumes/sohan-chitte-java-9yoe-resume-latest.pdf"
    }

    for file in files:
        loader = PyPDFLoader(files[file])
        docs = loader.load()
        content = "\n".join([doc.page_content for doc in docs])
        resumes[file] = " ".join(content.split())
        print(f"Resume - {file} loaded successfully.")

    print(f"no of resumes found - {len(resumes)}")
    return resumes