from __future__ import annotations

from app.orchestrator.state import BuilderState
from app.validators.validation_engine import validate_spec


def validation_agent(state: BuilderState) -> BuilderState:
    result = validate_spec(state.spec)
    state.validation = result
    return state

