FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libcairo2-dev pkg-config \
    postgresql-client curl libcairo2 gosu && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh && \
    mkdir -p /vol/static /vol/media && \
    useradd --system --home /app waterpark && \
    chown -R waterpark:waterpark /app /vol /start.sh

EXPOSE 8000
ENTRYPOINT ["/start.sh"]