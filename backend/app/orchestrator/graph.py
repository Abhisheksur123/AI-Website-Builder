from __future__ import annotations

from typing import Any, Dict, List, Optional

from langgraph.graph import StateGraph, END

from app.orchestrator.state import BuilderState
from app.agents.conversation_agent import conversation_agent
from app.agents.website_planner_agent import website_planner_agent
from app.agents.database_planner_agent import database_planner_agent
from app.agents.seo_admin_agent import seo_admin_agent
from app.validators.validation_agent import validation_agent
from app.agents.builder_execution_agent import builder_execution_agent


def _merge_dicts(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in updates.items():
        if v is None:
            continue
        if isinstance(v, list) and isinstance(out.get(k), list):
            out[k] = out.get(k, []) + v
        else:
            out[k] = v
    return out


def run_website_builder(req: Any) -> Dict[str, Any]:
    """Run the LangGraph workflow synchronously.

    This function is intentionally small; the LangGraph graph itself is declared in `build_graph()`.
    """
    graph = build_graph()

    initial_state: BuilderState = BuilderState(
        session_id=req.session_id,
        user_prompt=req.user_prompt,
        user_clarifications=req.user_clarifications or {},
        conversation={}
    )

    final_state = graph.invoke(initial_state, config={"recursion_limit": 10})

    # LangGraph returns an AddableValuesDict-like object, so convert to plain dict.
    if hasattr(final_state, "to_response_dict"):
        return final_state.to_response_dict()  # type: ignore[attr-defined]
    return dict(final_state)



def build_graph():
    graph = StateGraph(BuilderState)

    graph.add_node("conversation_agent", conversation_agent)
    graph.add_node("website_planner", website_planner_agent)
    graph.add_node("database_planner", database_planner_agent)
    graph.add_node("seo_admin", seo_admin_agent)
    graph.add_node("validate", validation_agent)
    graph.add_node("execute", builder_execution_agent)

    # Entry
    graph.set_entry_point("conversation_agent")

    # After conversation, we always attempt planning.
    graph.add_edge("conversation_agent", "website_planner")

    graph.add_edge("website_planner", "database_planner")
    graph.add_edge("database_planner", "seo_admin")
    graph.add_edge("seo_admin", "validate")

    def route_after_validation(state: BuilderState) -> str:
        # For this prototype, we stop after the first validation pass.
        # (A production system would route back to targeted repair agents.)
        if state.validation.get("is_valid") is True:
            return "execute"
        return "execute"

    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {"execute": "execute"},
    )


    graph.add_edge("execute", END)

    # Retries: LangGraph doesn't have a direct "retry" primitive; we model it with step limits.
    return graph.compile()

