# ──────────────────────────────────────────────────────────────
# Stage 1 – dependency cache
# Uses a stub src/ so pip resolves and installs runtime
# dependencies before copying real source code.
# This layer is only invalidated when pyproject.toml changes.
# ──────────────────────────────────────────────────────────────
FROM python:3.14-slim AS deps

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
# Receives only the installed packages; no pip, no build tools.
# ──────────────────────────────────────────────────────────────
FROM python:3.14-slim AS runtime

# Remove packages not needed by uvicorn/fastapi that carry unpatched CVEs.
# perl-base:   CVE-2026-42496 (CRITICAL), CVE-2026-8376 (CRITICAL),
#              CVE-2026-42497/48962/9538 (HIGH) — Perl is not needed at all.
# ncurses-bin: CVE-2025-69720 (HIGH) — CLI utilities, not the runtime lib.
# ncurses-base: CVE-2025-69720 (HIGH) — terminfo data, not required for a server.
RUN apt-get purge -y --allow-remove-essential --auto-remove \
      perl-base \
      ncurses-bin \
      ncurses-base && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser

WORKDIR /app

COPY --from=builder /install /usr/local

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
