# Backend (FastAPI + LangGraph)

## Run
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

## API
- `POST /api/chat`

### Request
```json
{
  "user_prompt": "Create an ecommerce website for ..."
}
```

### Response
```json
{
  "session_id": null,
  "clarification_questions": [],
  "spec": {"website_type": "ecommerce", "pages": [], "components": [], "entities": [], "admin_features": [], "seo": {}},
  "validated": {"is_valid": true, "missing": [], "dependency_issues": [], "confidence": {"overall": 0.95}},
  "builder_actions": [],
  "preview": {"cards": []}
}
```

