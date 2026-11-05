# 完整接口自动化（testcases 全部用例，不限 smoke）+ HTML/JUnit + 企业微信
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $here "run_scheduled_api_test.ps1") -Full @args
