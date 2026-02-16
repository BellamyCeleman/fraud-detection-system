# BUILDER STAGE
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Donwload everything we need to compile dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --compile-bytecode

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    netcat-openbsd \
    default-jre \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Take venv from the BUILDER
COPY --from=builder /app/.venv /app/.venv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY . .

RUN chmod +x entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV=/app/.venv
ENV SPARK_HOME=/app/.venv/lib/python3.12/site-packages/pyspark
ENV PATH="$PATH:$SPARK_HOME/bin"

ENTRYPOINT ["./entrypoint.sh"]