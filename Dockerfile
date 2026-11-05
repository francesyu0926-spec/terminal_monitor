FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    SCHEDULE_INTERVAL_SECONDS=900 \
    PYTEST_SCHEDULE_MARKERS=smoke

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_tests ./api_tests
COPY pytest.ini .
COPY scripts ./scripts

RUN chmod +x /app/scripts/docker_entrypoint.sh \
    && mkdir -p /app/reports/scheduled

VOLUME ["/app/reports"]

# 默认：每 15 分钟执行 pytest 并推送企业微信（环境变量与 .env 由 compose 注入）
ENTRYPOINT ["/app/scripts/docker_entrypoint.sh"]
