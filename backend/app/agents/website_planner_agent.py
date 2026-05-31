from __future__ import annotations

from typing import Any, Dict, List

from app.orchestrator.state import BuilderState


def website_planner_agent(state: BuilderState) -> BuilderState:
    website_type = state.conversation.get("website_type") or state.spec.get("website_type")
    wants_admin = state.conversation.get("requirements", {}).get("wants_admin", False)

    if website_type == "ecommerce":
        pages = [
            {"id": "home", "route": "/", "title": "Home"},
            {"id": "products", "route": "/products", "title": "Products"},
            {"id": "product_detail", "route": "/products/:productId", "title": "Product Details"},
            {"id": "cart", "route": "/cart", "title": "Cart"},
            {"id": "checkout", "route": "/checkout", "title": "Checkout"},
            {"id": "orders", "route": "/account/orders", "title": "Orders"},
        ]

        # Admin/login routes (needed for validation when admin/auth is requested)
        if wants_admin:
            pages.extend([
                {"id": "admin_login", "route": "/admin/login", "title": "Admin Login"},
                {"id": "admin_dashboard", "route": "/admin/dashboard", "title": "Admin Dashboard"},
                {"id": "admin", "route": "/admin", "title": "Admin"},
            ])

        components = [
            {"id": "product_card", "type": "ProductCard"},
            {"id": "product_grid", "type": "ProductGrid", "children": ["product_card"]},
            {"id": "cart_item_row", "type": "CartItemRow"},
            {"id": "checkout_summary", "type": "CheckoutSummary"},
        ]

        user_flows = [
            {"id": "browse_and_cart", "steps": ["home", "products", "product_detail", "cart"]},
            {"id": "checkout_flow", "steps": ["cart", "checkout", "orders"]},
        ]

        state.spec = _upsert(state.spec, {
            "pages": pages,
            "components": components,
            "user_flows": user_flows,
        })
    else:
        pages = [{"id": "home", "route": "/", "title": "Home"}]
        if wants_admin:
            pages.extend([
                {"id": "admin_login", "route": "/admin/login", "title": "Admin Login"},
                {"id": "admin_dashboard", "route": "/admin/dashboard", "title": "Admin Dashboard"},
                {"id": "admin", "route": "/admin", "title": "Admin"},
            ])

        state.spec = _upsert(state.spec, {
            "pages": pages,
            "components": [],
            "user_flows": [],
        })

    return state



def _upsert(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in updates.items():
        out[k] = v
    return out

