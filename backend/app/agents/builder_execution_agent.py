from __future__ import annotations

from typing import Any, Dict, List

from app.orchestrator.state import BuilderState


def builder_execution_agent(state: BuilderState) -> BuilderState:
    """Convert validated plan into builder_actions and a preview model."""

    pages = state.spec.get("pages", [])
    entities = state.spec.get("entities", [])

    builder_actions: List[Dict[str, Any]] = []

    # Page creation actions
    for p in pages:
        builder_actions.append({
            "action": "create_page",
            "page_id": p.get("id"),
            "route": p.get("route"),
            "title": p.get("title"),
        })

    # Entity (CMS/database) actions
    for e in entities:
        builder_actions.append({
            "action": "create_entity",
            "entity": e.get("name"),
            "fields": e.get("fields", []),
        })

    preview_cards = []
    # Render basic cards: one per page
    for p in pages[:6]:
        preview_cards.append({
            "title": p.get("title"),
            "subtitle": p.get("route"),
            "kind": "page_preview",
        })

    state.builder_actions = builder_actions
    state.preview = {
        "cards": preview_cards,
        "summary": {
            "pages": len(pages),
            "entities": len(entities),
        },
    }

    return state

