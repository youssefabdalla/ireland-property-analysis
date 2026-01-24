# --- STAGE 1: BUILDER ---
FROM python:3.12-slim as builder
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
# We build the 'meal' here (the .venv folder)
RUN poetry config virtualenvs.in-project true && poetry install

# --- STAGE 2: RUNTIME ---
FROM python:3.12-slim
WORKDIR /app
# We only take the 'finished plate' from the builder
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

# Tell Python to use the virtual environment we copied
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "src/main.py"]