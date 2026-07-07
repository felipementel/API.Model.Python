# ──────────────────────────────────────────────────────────────
# Stage 1 – dependency cache
# Uses a stub src/ so pip resolves and installs runtime
# dependencies before copying real source code.
# This layer is only invalidated when pyproject.toml changes.
# ──────────────────────────────────────────────────────────────
FROM python:3.14-alpine AS deps

WORKDIR /build

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml .

RUN mkdir -p src && \
    touch src/__init__.py && \
    pip install --no-cache-dir --prefix=/install . && \
    rm -rf src

# ──────────────────────────────────────────────────────────────
# Stage 2 – install application code (no deps, already cached)
# Only re-runs when src/ changes.
# ──────────────────────────────────────────────────────────────
FROM deps AS builder

COPY src ./src

RUN pip install --no-cache-dir \
      --prefix=/install \
      --no-deps \
      .

# ──────────────────────────────────────────────────────────────
# Stage 3 – minimal runtime image
# Alpine does not include perl, ncurses-bin, ncurses-base,
# and uses its own sqlite/ncurses packages without the CVEs
# present in the Debian slim variant.
# ──────────────────────────────────────────────────────────────
FROM python:3.14-alpine AS runtime

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /install /usr/local

USER appuser

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080"]
