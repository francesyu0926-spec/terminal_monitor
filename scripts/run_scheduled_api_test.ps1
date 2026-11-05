# 定时任务入口：执行 pytest 并将结果推送到企业微信
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Get-DotEnvValue {
    param([string]$Name)
    $path = Join-Path $Root ".env"
    if (-not (Test-Path $path)) { return "" }
    foreach ($line in Get-Content $path -Encoding UTF8) {
        $t = $line.Trim()
        if ($t -eq "" -or $t.StartsWith("#")) { continue }
        if ($t -match "^\s*$([regex]::Escape($Name))\s*=\s*(.*)\s*$") {
            return $Matches[1].Trim().Trim('"').Trim("'")
        }
    }
    return ""
}

$webhook = $env:WEWORK_WEBHOOK_URL
if (-not $webhook) { $webhook = Get-DotEnvValue "WEWORK_WEBHOOK_URL" }
if (-not $webhook) {
    Write-Error "未配置 WEWORK_WEBHOOK_URL（环境变量或 .env）"
}

$markers = $env:PYTEST_SCHEDULE_MARKERS
if (-not $markers) { $markers = Get-DotEnvValue "PYTEST_SCHEDULE_MARKERS" }
if (-not $markers) { $markers = "smoke" }

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& ".venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt | Out-Null

New-Item -ItemType Directory -Force -Path "reports\scheduled" | Out-Null
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$fileStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logPath = "reports\scheduled\run-$fileStamp.log"

$pytestArgs = @(
    "-m", $markers,
    "--tb=line",
    "-q",
    "api_tests/testcases/test_quotes_api.py"
)

Write-Host "[$stamp] pytest -m `"$markers`" ..."
$output = & pytest @pytestArgs 2>&1 | Out-String
$exitCode = $LASTEXITCODE
$output | Set-Content -Path $logPath -Encoding UTF8

$status = if ($exitCode -eq 0) { "通过" } else { "失败" }

$tail = ($output -split "`n" | Where-Object { $_.Trim() -ne "" } | Select-Object -Last 8) -join "`n"
if ($tail.Length -gt 1500) {
    $tail = $tail.Substring($tail.Length - 1500)
}

$content = @"
### 接口自动化巡检 · $status
> 时间：$stamp
> 项目：terminal_monitor
> 用例：-m $markers（test_quotes_api.py）
> 退出码：$exitCode

**pytest 摘要**
$tail

日志：reports/scheduled/run-$fileStamp.log
"@

$verifySsl = Get-DotEnvValue "VERIFY_SSL"
$insecureFlag = @()
if ($verifySsl -eq "false") { $insecureFlag = @("--insecure") }

$notifyFile = Join-Path $env:TEMP "wework-notify-$fileStamp.md"
Set-Content -Path $notifyFile -Value $content -Encoding UTF8
$notifyBody = Get-Content -Path $notifyFile -Raw -Encoding UTF8

python (Join-Path $Root "scripts\notify_wework.py") `
    --webhook $webhook `
    --content $notifyBody `
    @insecureFlag

exit $exitCode
