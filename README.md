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
| `TOKEN_HEADER` | token 请求头名称 | `token` |
| `TOKEN_PREFIX` | token 前缀（如 `Bearer `） | 空 |
| `API_TIMEOUT` | 超时（秒） | `30` |
| `API_TOKEN` | 静态 token（可选，跳过登录） | 空 |
| `HEALTH_PATH` | 健康检查路径（可选） | 空 |

## 鉴权说明

1. 用例会话开始时调用 `POST {API_BASE_URL}{API_PREFIX}/login/pwd`（`application/x-www-form-urlencoded`）。
2. 从响应 `data.token` 读取 JWT，写入请求头（默认 `token: <jwt>`）。
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

示例：`pytest -m "smoke and terminal"`

## CI

`.github/workflows/api-tests.yml` 在 push/PR 时运行冒烟用例。在仓库 Variables / Secrets 中配置 `API_BASE_URL`、`API_PREFIX`、`API_TOKEN` 等即可对接真实环境。
