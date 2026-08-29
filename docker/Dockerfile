# syntax=docker/dockerfile:1

# Keep uv in the build stage; the runtime image only receives the virtualenv.
FROM ghcr.io/astral-sh/uv:0.8.22 AS uv

FROM python:3.14-alpine AS builder

COPY --from=uv /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install locked runtime dependencies before copying source for better caching.
COPY source/pyproject.toml source/uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY source/src ./src
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.14-alpine AS runtime

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080"]
