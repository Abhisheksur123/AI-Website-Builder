from __future__ import annotations

from typing import Any, Dict

from app.orchestrator.state import BuilderState


def database_planner_agent(state: BuilderState) -> BuilderState:
    website_type = state.conversation.get("website_type")
    needs_payment = state.conversation.get("requirements", {}).get("needs_payment", False)

    entities = []
    relationships = []
    cms = {}

    if website_type == "ecommerce":
        entities = [
            {"name": "Product", "fields": ["id", "title", "price", "description", "sku", "image_url"]},
            {"name": "Inventory", "fields": ["id", "product_id", "quantity_available", "status"]},
            {"name": "Cart", "fields": ["id", "user_id", "created_at"]},
            {"name": "CartItem", "fields": ["id", "cart_id", "product_id", "quantity"]},
            {"name": "Order", "fields": ["id", "user_id", "total", "status", "created_at"]},
            {"name": "OrderItem", "fields": ["id", "order_id", "product_id", "quantity", "unit_price"]},
        ]

        relationships = [
            {"from": "Inventory", "to": "Product", "type": "many_to_one"},
            {"from": "CartItem", "to": "Cart", "type": "many_to_one"},
            {"from": "CartItem", "to": "Product", "type": "many_to_one"},
            {"from": "OrderItem", "to": "Order", "type": "many_to_one"},
            {"from": "OrderItem", "to": "Product", "type": "many_to_one"},
        ]

        if needs_payment:
            entities.append({"name": "Payment", "fields": ["id", "order_id", "provider", "amount", "status"]})

        cms = {
            "collections": ["products"],
            "references": {"product": ["inventory"]},
        }

    state.spec = {
        **state.spec,
        "entities": entities,
        "relationships": relationships,
        "cms": cms,
    }
    return state

