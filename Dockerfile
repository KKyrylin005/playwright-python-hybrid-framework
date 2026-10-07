# Image tag must match the playwright package version: browsers are baked into the image
ARG PLAYWRIGHT_VERSION=1.63.0
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

# Dependencies first: this layer is rebuilt only when pyproject.toml changes
COPY pyproject.toml ./
RUN python3 -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requirements.txt \
    && pip install -r /tmp/requirements.txt "playwright==${PLAYWRIGHT_VERSION}"

COPY README.md ./
COPY src ./src
RUN pip install --no-deps .

COPY --chown=pwuser:pwuser pytest.ini ./
COPY --chown=pwuser:pwuser tests ./tests

# Non-root user shipped with the Playwright image
USER pwuser

ENTRYPOINT ["python3", "-m", "pytest"]
CMD ["-n", "auto"]
