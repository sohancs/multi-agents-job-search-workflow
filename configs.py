import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="app.env")

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

JOB_SEARCH_QUERIES = os.getenv("JOB_SEARCH_QUERIES", ["Senior Backend Developer", "AI Engineer"])

LOCATION = os.getenv("LOCATION", "Dubai")
SEACH_JOB_COUNT = os.getenv("SEACH_JOB_COUNT", 10)

CANDIDATE_NAME = os.getenv("CANDIDATE_NAME")
CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL")
CANDIDATE_LINKEDIN_URL = os.getenv("CANDIDATE_LINKEDIN_URL")
CANDIDATE_GITHUB_URL = os.getenv("CANDIDATE_GITHUB_URL")
CANDIDATE_MOB_NO = os.getenv("CANDIDATE_MOB_NO")