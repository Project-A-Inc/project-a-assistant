
FROM python:3.12-slim
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main
COPY src /app/src
CMD ["poetry", "run", "uvicorn", "project_a_assistant.api:app", "--host", "0.0.0.0", "--port", "8000"]
