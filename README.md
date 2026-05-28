# AI Multi-Agent Drag-and-Drop Website Builder (LangGraph + FastAPI)

## Problem Statement
Design a practical AI multi-agent system that takes a high-level natural language request (e.g., “Create an ecommerce website…”) and produces a structured website-building plan suitable for a drag-and-drop website builder. The system must:
- Understand intent and extract requirements
- Ask follow-up questions when information is missing
- Break large requests into smaller planning tasks
- Generate structured JSON outputs (pages/components/entities/admin/SEO)
- Validate completeness and dependencies using explicit rules
- Convert validated plans into builder actions and a simple preview
- Orchestrate the above using a LangGraph workflow with reliable validation loops

> This repo focuses on AI orchestration and planning/validation pipelines (not complex frontend/drag-drop UX).

## Repository Structure
```
project-root/
│
├── frontend/
│   ├── (Next.js app)
│
├── backend/
│   ├── agents/
│   ├── orchestrator/
│   ├── validators/
│   ├── schemas/
│   ├── workflows/
│   └── api/
│
├── diagrams/
│   ├── architecture.mmd
│   ├── multi_agent_workflow.mmd
│   ├── validation_pipeline.mmd
│   └── builder_execution_flow.mmd
│
├── docs/
│   └── (optional notes)
│
└── README.md
```

## High-Level Architecture
The backend runs a LangGraph state machine. Each node uses a dedicated “agent” function (LLM-backed where configured; deterministic fallbacks for robustness) to:
1. Extract requirements + ask clarifications
2. Produce an initial website plan (pages/components/navigation/user flows)
3. Produce a data model (entities/relationships/CMS structures)
4. Produce SEO + admin features
5. Validate the plan for completeness + rule-based dependencies
6. If invalid, route back to the appropriate agent(s) with targeted repair instructions
7. Produce builder actions and a preview model

### Mermaid Diagrams
See `/diagrams/*.mmd`.

## Agent Responsibilities
1. **Conversation Agent**
   - Extracts intent (website type, goals)
   - Detects missing info and proposes clarification questions

2. **Orchestrator Agent**
   - Coordinates workflow state transitions
   - Merges partial outputs into a single draft “website spec”

3. **Website Planner Agent**
   - Generates pages, components, navigation, user flows

4. **Database Planner Agent**
   - Generates entities/relationships suitable for a builder backend/CMS

5. **SEO/Admin Agent**
   - Generates SEO metadata/sitemap planning
   - Plans admin/auth features and CMS management

6. **Validation Agent**
   - Applies explicit validation rules (ecommerce/payment/admin dependency checks)
   - Produces confidence scores and suggested fixes
   - Drives the repair loop when requirements are missing

7. **Builder Execution Agent**
   - Converts the validated spec into “builder_actions”
   - Produces a lightweight preview representation

## Workflow Lifecycle
**User Prompt → Understanding → Clarification Questions → Planning → Validation → Builder Action Generation → Website Preview**

## Validation Strategy (Key Rules)
Implemented with explicit rule checks over the structured plan.

Examples:
- If **payment exists** ⇒ checkout required; order entity required
- If **ecommerce** ⇒ product entity required; inventory required
- If **admin panel exists** ⇒ authentication required

The validator returns:
- `is_valid` boolean
- `missing` items
- `dependency_issues`
- `confidence` scores
- `repair_instructions` for the orchestrator/agents

## Scalability
- LangGraph makes it easy to extend:
  - Add new website types (restaurant/portfolio/booking/SaaS/blog)
  - Add more agents (e.g., payments provider integration)
  - Add more validators (security, performance budgets)
- State and partial outputs are stored/passed as structured JSON.

## Technical Decisions (Summary)
- **FastAPI**: clean API boundaries for chat, planning, and rendering
- **LangGraph**: deterministic control flow with conditional routing and loops
- **Pydantic**: enforce structured schemas for planner outputs
- **SQLite**: store conversations + generated specs/actions for auditability

## Setup Instructions
### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# (Optional) set OpenAI key
export OPENAI_API_KEY="..."

uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev --port 3000
```

### 3) Try the demo
- Open frontend at http://localhost:3000
- Submit a prompt like:
  > “Create an ecommerce website for my clothing brand with product listing, cart, checkout, payment integration, inventory management, offers, admin panel, and SEO support.”

## What This Prototype Demonstrates
- Multi-agent orchestration via LangGraph
- Conditional routing + validation repair loop
- Structured JSON planning outputs
- Builder action generation + simple preview model

## Notes / Next Steps
Once implemented, you can run:
- backend unit tests (if added)
- a scripted demo request to validate end-to-end correctness

