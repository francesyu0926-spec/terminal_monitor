#!/bin/sh
set -eu

cd /app
mkdir -p reports/scheduled

MARKERS="${PYTEST_SCHEDULE_MARKERS:-smoke}"
INTERVAL="${SCHEDULE_INTERVAL_SECONDS:-900}"
WEBHOOK="${WEWORK_WEBHOOK_URL:-}"

sleep_until_next_slot() {
  interval_sec="${1:-900}"
  interval_min=$((interval_sec / 60))
  if [ "$interval_min" -lt 1 ]; then
    interval_min=15
    interval_sec=900
  fi

  min=$((10#$(date +%M)))
  sec=$((10#$(date +%S)))
  elapsed=$(((min % interval_min) * 60 + sec))
  if [ "$elapsed" -eq 0 ]; then
    wait_sec=0
  else
    wait_sec=$((interval_sec - elapsed))
  fi

  if [ "$wait_sec" -gt 0 ]; then
    echo "对齐时钟：${wait_sec}s 后执行（每 ${interval_min} 分钟整点 :00/:15/:30/:45）"
    sleep "$wait_sec"
  fi
}

run_once() {
  stamp="$(date '+%Y-%m-%d %H:%M:%S')"
  file_stamp="$(date '+%Y%m%d-%H%M%S')"
  log_path="reports/scheduled/run-${file_stamp}.log"
  junit_path="reports/junit-${file_stamp}.xml"
  html_path="reports/full-report-${file_stamp}.html"

  echo "[$stamp] pytest -m ${MARKERS} ..."
  set +e
  pytest -m "$MARKERS" api_tests/testcases/test_quotes_api.py \
    --tb=short -ra \
    --junitxml="$junit_path" \
    --html="$html_path" --self-contained-html \
    >"$log_path" 2>&1
  exit_code=$?
  set -e

  if [ -n "$WEBHOOK" ] && [ -f "$junit_path" ]; then
    insecure=""
    if [ "${VERIFY_SSL:-true}" = "false" ]; then
      insecure="--insecure"
    fi
    if [ "$exit_code" -ne 0 ]; then
      pdf_short="$(date '+%Y%m%d_%H%M%S')"
      pdf_path="reports/wecom_failure_${pdf_short}.pdf"
      # shellcheck disable=SC2086
      python /app/scripts/wework_test_report.py \
        --webhook "$WEBHOOK" \
        --junit "$junit_path" \
        --stamp "$stamp" \
        --html "$html_path" \
        --log "$log_path" \
        --pdf-out "$pdf_path" \
        $insecure || true
    else
      # shellcheck disable=SC2086
      python /app/scripts/wework_test_report.py \
        --webhook "$WEBHOOK" \
        --junit "$junit_path" \
        --stamp "$stamp" \
        --html "$html_path" \
        --log "$log_path" \
        $insecure || true
    fi
  fi

  echo "[$stamp] 完成，exit=${exit_code}"
  return "$exit_code"
}

if [ "${RUN_MODE:-loop}" = "once" ]; then
  run_once
  exit $?
fi

echo "定时巡检启动：时钟对齐每 $((INTERVAL / 60)) 分钟，标记 ${MARKERS}"
while true; do
  sleep_until_next_slot "$INTERVAL"
  run_once || true
done
