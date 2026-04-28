import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="app.env")

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

RAW_JOB_SEARCH_QUERIES = os.getenv("JOB_SEARCH_QUERIES", "Senior Backend Developer, AI Engineer")
JOB_SEARCH_QUERIES = [query.strip() for query in RAW_JOB_SEARCH_QUERIES.split(",")]

RAW_LOCATION = os.getenv("LOCATION", "Dubai, United Arab Emirates")
LOCATION = [query.strip() for query in RAW_LOCATION.split(",")]

SEACH_JOB_COUNT = os.getenv("SEACH_JOB_COUNT", 10)
JOB_POSTED_FILTER_IN_SEC = os.getenv("JOB_POSTED_FILTER_IN_SEC", "r86400") #24 hrs filter

CANDIDATE_NAME = os.getenv("CANDIDATE_NAME")
CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL")
CANDIDATE_LINKEDIN_URL = os.getenv("CANDIDATE_LINKEDIN_URL")
CANDIDATE_GITHUB_URL = os.getenv("CANDIDATE_GITHUB_URL")
CANDIDATE_MOB_NO = os.getenv("CANDIDATE_MOB_NO")