# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install system tools needed to compile psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into a specific path (compile bytecode for speed)
RUN uv sync --frozen --no-dev --compile-bytecode

# --- Stage 2: Final Runtime Stage ---
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed environment from the builder
COPY --from=builder /app/.venv /app/.venv
COPY . .

RUN chmod +x entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "main.py"]