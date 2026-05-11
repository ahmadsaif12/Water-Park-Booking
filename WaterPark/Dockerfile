# Stage 1: Builder
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev libcairo2-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM python:3.12-slim AS runtime

ARG ENVIRONMENT=dev
ENV ENVIRONMENT=${ENVIRONMENT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client curl netcat-openbsd libcairo2 gosu \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

WORKDIR /app
COPY . /app
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /vol/static /vol/media \
    && groupadd --system waterpark \
    && useradd --system --gid waterpark --home /app waterpark \
    && chown -R waterpark:waterpark /app /vol /start.sh



HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000
ENTRYPOINT ["/start.sh"]