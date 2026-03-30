## Section A — Team Task Breakdown

### Team and roles
- **Tech Lead (me)**: owns architecture, integration decisions, code review/merge, and delivery quality.
- **Intern 1**: owns domain logic + unit tests (fast feedback, low external dependency).
- **Intern 2**: owns integration layers (model/LLM adapters, CLIs), plus “happy path” demos.

### How I’d split Task 1 (Inspection Service)
- **Intern 1 (Domain + tests)**:
  - Define the JSON contract as typed domain models (status, confidence, recommendation).
  - Implement the decision rule (threshold → DEFECT_DETECTED/NO_DEFECT_DETECTED).
  - Write unit tests for decision logic and input validation edge cases.
- **Intern 2 (Infra + interface)**:
  - Implement the Ultralytics YOLOE adapter (model load, `set_classes`, `predict`) and map results to domain detections.
  - Build the CLI and error handling for file-not-found, unsupported formats, and timeouts.
  - Provide a sample command and a “works on my machine” run-through.
- **Tech Lead (Architecture + review)**:
  - Set DDD boundaries (domain/application/infrastructure/interfaces) and define port interfaces.
  - Decide how to measure processing time and what “confidence” means (max detection confidence).
  - Review PRs for correctness, style, and edge-case handling; keep the output schema stable.

### How I’d split Task 2 (LLM Insight Layer)
- **Intern 1 (Schemas + fallback)**:
  - Define Pydantic schemas for Task 1 output and the manager-facing response.
  - Implement deterministic fallback messaging for LLM failures (API down/missing key).
  - Add unit tests for fallback (no network required).
- **Intern 2 (LangChain + CLI)**:
  - Implement LangChain OpenAI adapter (load `.env` via python-dotenv; never hardcode keys).
  - Store the prompt as a first-class constant (not embedded in business logic).
  - Build CLI that accepts JSON file or stdin and prints only the final plain-English insight.
- **Tech Lead (Prompting + product quality)**:
  - Ensure prompt is clear, manager-friendly, and enforces structured output parsing.
  - Validate that we parse and return clean text (not raw dumps), and that failure modes are safe.
  - Final review: security (no keys in repo), consistency with Task 1 contract, and usability.

### Why this split works
- Maximizes parallelism: domain/test work proceeds independently from model/LLM integration.
- Keeps interns in bounded, testable scopes while the TL handles cross-cutting decisions.
- Reduces risk: deterministic fallback + unit tests provide a reliable baseline even if APIs/models are flaky.

### Daily standup (10 minutes, timeboxed)
- **Format** (each person ≤ 90 seconds):
  - What I shipped yesterday (PRs merged or ready).
  - What I’ll ship today (specific file/module outcomes).
  - Blockers (need decisions, API access, model download, unclear requirements).
- **Blocker policy**:
  - Anything blocked > 30 minutes gets escalated immediately in a thread; TL resolves within same day.
- **Definition of done**:
  - Unit test added/updated, CLI run example works, error paths are handled, output contract unchanged.

## Section B

Prompt not provided in the task statement; intentionally left minimal to avoid guessing requirements.

## Section C

Prompt not provided in the task statement; intentionally left minimal to avoid guessing requirements.
