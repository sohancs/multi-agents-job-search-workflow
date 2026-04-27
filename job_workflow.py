from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes.scrapper_node import scrap_jobs
from nodes.filter_node import filter_jobs
from nodes.load_resume_node import resume_loader
from nodes.db_writter_node import db_writter_fn, update_job_status
from agents.reranker_agent import rerank_jobs
from agents.resume_selector_agent import resume_selector
from nodes.draft_email_node import draft_email_node_fn
from agents.email_writter_agent import write_email_agent_fn

def build_workflow():
    """Build the job search workflow."""
    graph = StateGraph(AgentState)

    graph.add_node("scrap_jobs", scrap_jobs)
    graph.add_node("filter_jobs", filter_jobs)
    graph.add_node("db_writter_fn", db_writter_fn)
    graph.add_node("rerank_jobs", rerank_jobs)
    graph.add_node("resume_selector", resume_selector)
    graph.add_node("draft_email_node_fn", draft_email_node_fn)
    graph.add_node("update_job_status", update_job_status)
    graph.add_node("write_email_agent_fn", write_email_agent_fn)

    graph.add_edge(START, "scrap_jobs")
    graph.add_edge("scrap_jobs", "filter_jobs")
    graph.add_edge("filter_jobs", "resume_selector")
    graph.add_edge("resume_selector", "rerank_jobs")
    graph.add_edge("rerank_jobs", "db_writter_fn")
    graph.add_edge("rerank_jobs", "write_email_agent_fn")
    graph.add_edge("db_writter_fn", END)
    graph.add_edge("write_email_agent_fn", "draft_email_node_fn")
    graph.add_edge("draft_email_node_fn", "update_job_status")
    graph.add_edge("update_job_status", END)

    return graph.compile()