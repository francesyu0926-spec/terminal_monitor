# 完整行情接口测试 + HTML 报告 + 企业微信（成败均通知）
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $here "run_scheduled_api_test.ps1") -Full @args
