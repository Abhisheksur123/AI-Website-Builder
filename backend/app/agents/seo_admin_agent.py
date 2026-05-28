from __future__ import annotations

from typing import Any, Dict

from app.orchestrator.state import BuilderState


def seo_admin_agent(state: BuilderState) -> BuilderState:
    website_type = state.conversation.get("website_type")
    wants_admin = state.conversation.get("requirements", {}).get("wants_admin", False)

    seo = {
        "site_name": "AI Website Builder",
        "default_title": "AI Website Builder",
        "meta_description": "Generated website plan",
        "sitemap": {
            "include_routes": []
        },
    }

    pages = state.spec.get("pages", [])
    seo["sitemap"]["include_routes"] = [p.get("route") for p in pages if p.get("route")]

    admin_features = []
    if wants_admin:
        admin_features = [
            {"id": "auth", "type": "authentication"},
            {"id": "content_management", "type": "cms"},
            {"id": "inventory_management", "type": "inventory"},
            {"id": "order_management", "type": "orders"},
        ]

    state.spec = {
        **state.spec,
        "seo": seo,
        "admin_features": admin_features,
    }

    return state

