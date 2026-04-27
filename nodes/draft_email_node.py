from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from state import AgentState
import os
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from configs import CANDIDATE_EMAIL
import base64

def draft_email_service(to_email: str, subject: str, body: str) -> dict:
    """Draft email to be sent to the recruiter for each job application."""

    try:
        msg = MIMEText(body, 'plain')
        msg['to'] = to_email
        msg['subject'] = subject
        msg['from'] = CANDIDATE_EMAIL

        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        draft = {
            "message" : {
                "raw" : raw_msg
            }
        }
        gmail_client = get_gmail_credentials()
        gmail_response = gmail_client.users().drafts().create(userId='me', body=draft).execute()
        print(f"Drafted email to {to_email} with subject {subject}")
        return {"success" : gmail_response}
    except Exception as ex:
        print(f"failed to draft email for {to_email} with subject {subject} - {ex}")
        return {"error": str(ex)}
    

def get_gmail_credentials() :
    """Authenticate and get Gmail API credentials."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

    cred = None
    if os.path.exists('secrets/token.json') :
        cred = Credentials.from_authorized_user_file('secrets/token.json', SCOPES)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else :
            flow = InstalledAppFlow.from_client_secrets_file('secrets/credentials.json', SCOPES)
            cred = flow.run_local_server(port=0)
        
        with open('secrets/token.json', 'w') as token:
            token.write(cred.to_json())
    
    service = build('gmail', 'v1', credentials=cred)
    
    return service

def draft_email_node_fn(state: AgentState) -> dict:
    """Node function to draft email for each of the reranked jobs."""
    mail_drafts = state.get("mail_drafts", [])
    
    for job in mail_drafts:      
        draft_response = draft_email_service(job.get("recruiter_email",""), job.get("subject",""), job.get("body",""))
        job["email_draft_response"] = "success" if draft_response.__contains__("success") else "failure"

    return {"mail_drafts" : mail_drafts}