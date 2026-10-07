# Image tag must match the playwright version in poetry.lock: browsers are baked into the image
ARG PLAYWRIGHT_VERSION=1.63.0

# ---------- stage 1: pinned requirements from poetry.lock ----------
FROM python:3.12-slim AS requirements
RUN pip install --no-cache-dir "poetry==2.5.1" poetry-plugin-export
WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN poetry export --only main --without-hashes --output requirements.txt

# ---------- stage 2: test runner ----------
FROM mcr.microsoft.com/playwright/python:v${PLAYWRIGHT_VERSION}-noble

ARG PLAYWRIGHT_VERSION
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Single-purpose container: installing into the system interpreter is intended
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    E2E_HEADLESS=true

WORKDIR /app
RUN chown pwuser:pwuser /app

# Dependencies first: this layer is rebuilt only when poetry.lock changes
COPY --from=requirements /build/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt \
    && python3 -c "import importlib.metadata as m, sys; v = m.version('playwright'); \
sys.exit(0 if v == '${PLAYWRIGHT_VERSION}' else f'playwright {v} in lock != image ${PLAYWRIGHT_VERSION}')"

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-deps .

COPY --chown=pwuser:pwuser pytest.ini ./
COPY --chown=pwuser:pwuser tests ./tests

# Non-root user shipped with the Playwright image
USER pwuser

ENTRYPOINT ["python3", "-m", "pytest"]
CMD ["-n", "auto"]
