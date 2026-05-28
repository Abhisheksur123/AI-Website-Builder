from __future__ import annotations

from typing import Any, Dict, List, Tuple


def validate_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based validation.

    Returns:
    {
      is_valid: bool,
      missing: [...],
      dependency_issues: [...],
      confidence: {rule: float},
      repair_instructions: [...]
    }
    """

    website_type = spec.get("website_type")
    admin_features = spec.get("admin_features", [])
    pages = spec.get("pages", [])
    entities = spec.get("entities", [])

    entity_names = {e.get("name") for e in entities if isinstance(e, dict)}
    page_ids = {p.get("id") for p in pages if isinstance(p, dict)}

    has_payment = any("Payment" == n for n in entity_names)

    missing: List[str] = []
    dependency_issues: List[str] = []

    confidence = {
        "overall": 0.7,
        "rules": 0.8,
    }

    repair_instructions: List[str] = []

    # Payment dependencies
    if has_payment:
        if "checkout" not in page_ids:
            missing.append("checkout_page")
            dependency_issues.append("Payment entity requires checkout page")
            repair_instructions.append("Add checkout page route /checkout and connect payment flow to it.")
        if "Order" not in entity_names:
            missing.append("order_entity")
            dependency_issues.append("Payment entity requires Order entity")
            repair_instructions.append("Add Order + OrderItem entities and ensure Payment references Order.")

    # Ecommerce dependencies
    if website_type == "ecommerce":
        if "Product" not in entity_names:
            missing.append("product_entity")
            dependency_issues.append("Ecommerce requires Product entity")
            repair_instructions.append("Add Product entity with fields title/price/description/sku/image_url.")
        if "Inventory" not in entity_names:
            missing.append("inventory_entity")
            dependency_issues.append("Ecommerce requires Inventory entity")
            repair_instructions.append("Add Inventory entity linked to Product with quantity_available.")
        # Cart dependency
        if "Cart" not in entity_names or "CartItem" not in entity_names:
            missing.append("cart_entities")
            dependency_issues.append("Ecommerce requires Cart and CartItem")
            repair_instructions.append("Add Cart + CartItem entities." )

    # Admin panel dependencies
    admin_auth_required = any(f.get("id") == "auth" or f.get("type") == "authentication" for f in admin_features if isinstance(f, dict))
    if admin_features:
        if admin_auth_required:
            if not any(p.get("id") in {"admin", "login", "dashboard"} for p in pages if isinstance(p, dict)):
                missing.append("admin_auth_pages")
                dependency_issues.append("Admin/auth requires login/admin routes")
                repair_instructions.append("Add login/admin routes and authentication flow." )

    is_valid = len(missing) == 0 and len(dependency_issues) == 0

    if is_valid:
        confidence["overall"] = 0.95
    else:
        confidence["overall"] = 0.35

    return {
        "is_valid": is_valid,
        "missing": missing,
        "dependency_issues": dependency_issues,
        "confidence": confidence,
        "repair_instructions": repair_instructions,
    }

