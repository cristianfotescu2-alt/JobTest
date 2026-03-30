# Task 2 - LLM Conversational Insight Layer

This project adds a Python-only insight layer that turns Task 1 inspection JSON into plain-English guidance for a non-technical factory floor manager.

It uses:
- LangChain
- OpenAI chat model integration
- Pydantic output schema parsing
- python-dotenv for API key loading from `.env`

## Project structure

- `insight_service/domain`: schemas, errors, and LLM port
- `insight_service/application`: prompt, use case, fallback logic
- `insight_service/infrastructure`: LangChain OpenAI adapter
- `insight_service/interfaces`: CLI entrypoint
- `tests`: unit tests (no network/API required)

## Setup (conda, Python 3.12)

```bash
conda env create -f environment.yml
conda activate task2-insight
```

If needed:

```bash
pip install -r requirements.txt
```

## Configure API key

```bash
cp .env.example .env
```

Then set `OPENAI_API_KEY` in `.env`.

Optional:
- `OPENAI_MODEL=gpt-4o-mini` (or another chat model)

## Run

From JSON file:

```bash
python -m insight_service.interfaces.cli --task1-json /path/to/task1_output.json
```

From stdin:

```bash
cat /path/to/task1_output.json | python -m insight_service.interfaces.cli
```

## Run tests

```bash
pytest -q
```

## Notes

- The manager-facing insight is returned cleanly, not raw LLM output.
- A deterministic fallback message is returned when the LLM API is unavailable.
- AI coding assistance disclosure:
  - This codebase was developed with assistance from Cursor AI tooling.
