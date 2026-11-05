#!/bin/sh
set -eu

cd /app
mkdir -p reports/scheduled

MARKERS="${PYTEST_SCHEDULE_MARKERS:-smoke}"
INTERVAL="${SCHEDULE_INTERVAL_SECONDS:-900}"
WEBHOOK="${WEWORK_WEBHOOK_URL:-}"

notify_wework() {
  content="$1"
  if [ -z "$WEBHOOK" ]; then
    echo "[warn] 未设置 WEWORK_WEBHOOK_URL，跳过企业微信通知"
    return 0
  fi
  insecure=""
  if [ "${VERIFY_SSL:-true}" = "false" ]; then
    insecure="--insecure"
  fi
  # shellcheck disable=SC2086
  python /app/scripts/notify_wework.py --webhook "$WEBHOOK" --content "$content" $insecure
}

run_once() {
  stamp="$(date '+%Y-%m-%d %H:%M:%S')"
  file_stamp="$(date '+%Y%m%d-%H%M%S')"
  log_path="reports/scheduled/run-${file_stamp}.log"

  echo "[$stamp] pytest -m ${MARKERS} ..."
  set +e
  pytest -m "$MARKERS" --tb=line -q api_tests/testcases/test_quotes_api.py >"$log_path" 2>&1
  exit_code=$?
  set -e

  if [ "$exit_code" -eq 0 ]; then
    status="通过"
  else
    status="失败"
  fi

  tail_text="$(tail -n 8 "$log_path" 2>/dev/null || true)"
  content="### 接口自动化巡检 · ${status}
> 时间：${stamp}
> 容器：terminal_monitor
> 用例：-m ${MARKERS}
> 退出码：${exit_code}

**pytest 摘要**
${tail_text}

日志：${log_path}"

  notify_wework "$content"
  echo "[$stamp] 完成，exit=${exit_code}"
  return "$exit_code"
}

# 单次模式：RUN_MODE=once（便于 CI / 手动 docker run）
if [ "${RUN_MODE:-loop}" = "once" ]; then
  run_once
  exit $?
fi

echo "定时巡检启动：每 ${INTERVAL}s 执行一次，标记 ${MARKERS}"
while true; do
  run_once || true
  sleep "$INTERVAL"
done
