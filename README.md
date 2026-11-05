# terminal_monitor

终端监控服务的接口自动化测试工程（pytest + httpx）。

## 目录结构

```
api_tests/
  config/          # 环境变量与全局配置
  core/            # HTTP 客户端与通用断言
  schemas/         # JSON Schema（响应契约）
  services/        # 按模块封装的 API 调用
  data/            # 测试数据（JSON）
  testcases/       # 用例
scripts/           # 本地运行脚本
.github/workflows/ # CI 示例
```

## 快速开始

1. 复制环境配置并修改被测地址：

   ```powershell
   copy .env.example .env
   ```

2. 安装依赖并执行冒烟用例：

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pytest -m smoke
   ```

   或使用脚本（会自动创建虚拟环境）：

   ```powershell
   .\scripts\run_api_tests.ps1
   ```

3. 生成 HTML 报告：

   ```powershell
   pytest -m regression --html=reports/report.html --self-contained-html
   ```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `API_BASE_URL` | 服务根 URL | `https://terminal.sfccn.com` |
| `API_PREFIX` | API 前缀 | `/terminal/zxt-web` |
| `LOGIN_CODE` | 登录账号 | 空（必填，除非用 `API_TOKEN`） |
| `LOGIN_PASSWORD` | 登录密码（加密后） | 空 |
| `LOGIN_PATH` | 登录路径 | `/login/pwd` |
| `TOKEN_TTL_SECONDS` | token 本地缓存时长 | `43200`（12 小时） |
| `AUTH_HEADERS` | 鉴权头列表（逗号分隔） | `Secret,Token` |
| `TOKEN_HEADER` | 单头模式（未设 AUTH_HEADERS 时） | 空 |
| `TOKEN_PREFIX` | token 前缀（如 `Bearer `） | 空 |
| `QUOTES_API_BASE` | 行情业务 API 根路径（desk） | `https://terminal.sfccn.com/terminal/desk/quotes/api` |
| `QUOTES_HEALTH_API_BASE` | 行情 health 旧路径根 | `https://terminal.sfccn.com/terminal/quotes/api` |
| `API_TIMEOUT` | 超时（秒） | `30` |
| `API_TOKEN` | 静态 token（可选，跳过登录） | 空 |
| `HEALTH_PATH` | 其它服务健康检查（可选） | 空 |

## 鉴权说明

1. 用例会话开始时调用 `POST {API_BASE_URL}{API_PREFIX}/login/pwd`（`application/x-www-form-urlencoded`）。
2. 从响应 `data.token` 读取 JWT，写入 `AUTH_HEADERS` 中的每个请求头（默认 `Secret`、`Token`）。
3. **12 小时内**复用同一 token（内存 + `.cache/api_token.json`），过期或收到 `401` 时自动重新登录。
4. 账号密码请只放在本地 `.env` 或 CI Secrets 中，**不要提交到 Git**。

## 默认接口约定

用例假设 REST 路径为 `{API_BASE_URL}{API_PREFIX}/terminals`，健康检查为 `{API_BASE_URL}{HEALTH_PATH}`。若与实际后端不一致，请修改：

- `api_tests/services/terminal_api.py` 中的路径
- `api_tests/schemas/terminal.py` 中的字段
- `api_tests/data/terminal_create.json` 中的请求体

## 标记（markers）

- `smoke`：冒烟
- `regression`：回归
- `health` / `terminal`：按模块筛选

示例：`pytest -m "smoke and quote"`

行情相关用例集中在 **`api_tests/testcases/test_quotes_api.py`**：

| 接口 | 测试函数 | 请求数据 |
|------|----------|----------|
| 登录 / Token | `test_login_*` | `.env` |
| `GET .../quotes/api/health` | `test_quotes_api_health` | `QUOTES_HEALTH_API_BASE` |
| `POST /quote` | `test_quote_single_symbol` | `data/quote_request.json` |
| `POST /catesorting` | `test_catesorting_paged_list` | `data/catesorting_request.json` |
| `POST /dayk` | `test_dayk_ohlc_series` | `data/dayk_request.json` |
| `POST /weekk` | `test_weekk_ohlc_series` | `data/weekk_request.json` |
| `POST /monthk` | `test_monthk_ohlc_series` | `data/monthk_request.json` |
| `POST /yeark` | `test_yeark_ohlc_series` | `data/yeark_request.json` |
| `POST /m1~m120` | `test_desk_intraday_ohlc_series`（参数化 6 个周期） | `data/desk_intraday_request.json` |
| `POST /astocksquote` | `test_desk_astocksquote` | `data/astocksquote_request.json`（空对象） |
| `POST /sectorMultipleSort` | `test_desk_sector_multiple_sort` | `data/sector_multiple_sort_request.json` |
| `POST /importantindex` | `test_desk_importantindex` | `data/importantindex_request.json` |
| `POST /profinmainindex` | `test_desk_profinmainindex` | `data/profinmainindex_request.json` |
| `POST /proincstatementnew` | `test_desk_proincstatementnew` | `data/proincstatementnew_request.json` |
| `POST /probalsheetnew` | `test_desk_probalsheetnew` | `data/probalsheetnew_request.json` |
| `POST /procfstatementnew` | `test_desk_procfstatementnew` | `data/procfstatementnew_request.json` |
| `POST /subnewstockranking` | `test_desk_subnewstockranking` | `data/subnewstockranking_request.json` |
| `POST /newsharescal` | `test_desk_newsharescal` | `data/newsharescal_request.json` |

以上 POST 接口均基于 **`QUOTES_API_BASE`**（默认 `/terminal/desk/quotes/api`）。

运行全部行情用例：`pytest api_tests/testcases/test_quotes_api.py -v`

## Docker 部署

前置：已安装 Docker / Docker Compose，项目根目录存在 `.env`（含登录与 `WEWORK_WEBHOOK_URL`）。

```bash
# 构建并启动定时巡检（每 15 分钟，后台运行）
docker compose up -d --build api-scheduler

# 查看日志
docker compose logs -f api-scheduler

# 单次冒烟（不进入循环）
docker compose --profile once run --rm api-test-once

# 停止
docker compose down
```

环境变量（可在 `docker-compose.yml` 或 `.env` 中调整）：

| 变量 | 说明 | 默认 |
|------|------|------|
| `SCHEDULE_INTERVAL_SECONDS` | 巡检间隔（秒） | `900` |
| `PYTEST_SCHEDULE_MARKERS` | pytest 标记 | `smoke` |
| `RUN_MODE` | `loop` 循环 / `once` 单次 | `loop` |

报告挂载到宿主机 `./reports/scheduled/`。

## 定时巡检（每 15 分钟 + 企业微信）

1. 在 `.env` 配置 `WEWORK_WEBHOOK_URL`（机器人 Webhook 完整地址）。
2. 可选：`PYTEST_SCHEDULE_MARKERS=smoke`（默认冒烟，避免 m1 等长用例拖慢周期）。
3. 手动跑一次：

   ```powershell
   .\scripts\run_scheduled_api_test.ps1
   ```

4. 注册 Windows 计划任务（**管理员 PowerShell**）：

   ```powershell
   .\scripts\register_scheduled_task.ps1
   ```

任务名：`TerminalMonitor-ApiTest-Every15Min`。**按时钟整点**每 15 分钟触发（:00 / :15 / :30 / :45），不是从注册或部署时刻起算；日志在 `reports/scheduled/`。已注册过旧任务请重新执行 `register_scheduled_task.ps1`。

## CI

`.github/workflows/api-tests.yml` 在 push/PR 时运行冒烟用例。在仓库 Variables / Secrets 中配置 `API_BASE_URL`、`API_PREFIX`、`API_TOKEN` 等即可对接真实环境。
