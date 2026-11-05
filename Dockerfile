FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    TZ=Asia/Shanghai \
    SCHEDULE_INTERVAL_SECONDS=900 \
    PYTEST_SCHEDULE_MARKERS=smoke

WORKDIR /app

RUN apk add --no-cache tzdata ca-certificates \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 敏感配置运行时注入：docker compose env_file .env（WEWORK_WEBHOOK_URL、LOGIN_CODE 等）
COPY api_tests ./api_tests
COPY pytest.ini .
COPY scripts ./scripts

RUN chmod +x /app/scripts/docker_entrypoint.sh \
    && mkdir -p /app/reports/scheduled

VOLUME ["/app/reports"]

# 时钟对齐每 15 分钟：pytest api_tests/testcases + 企业微信（见 docker_entrypoint.sh）
CMD ["sh", "scripts/docker_entrypoint.sh"]
