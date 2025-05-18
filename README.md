
# Project‑A Assistant

Conversational B2B sales assistant built with Python 3.12, Poetry, LangGraph and Azure OpenAI.

## Development quick‑start

```bash
# clone repo
poetry install                         # install runtime + dev dependencies
poetry config virtualenvs.in-project true --local
cp .env.example .env                   # add secrets
poetry run uvicorn project_a_assistant.api:app --reload
```

Swagger docs: <http://127.0.0.1:8000/docs>
