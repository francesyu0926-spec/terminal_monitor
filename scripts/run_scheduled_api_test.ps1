# 执行 pytest，生成 HTML/JUnit/PDF，并按参考模板推送企业微信（成功/失败均通知）
param(
    [switch]$Full,
    [switch]$SkipNotify
)

$ErrorActionPreference = "Continue"
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

$markers = $env:PYTEST_SCHEDULE_MARKERS
if (-not $markers) { $markers = Get-DotEnvValue "PYTEST_SCHEDULE_MARKERS" }
if (-not $markers) { $markers = "smoke" }

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& ".venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt 2>&1 | Out-Null

New-Item -ItemType Directory -Force -Path "reports\scheduled" | Out-Null
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$fileStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logPath = "reports\scheduled\run-$fileStamp.log"
$junitPath = "reports\junit-$fileStamp.xml"
$htmlReport = "reports\full-report-$fileStamp.html"

$exitCode = 1
$output = ""

try {
    $pytestArgs = @(
        "api_tests/testcases/test_quotes_api.py",
        "--tb=short",
        "-ra",
        "--junitxml=$junitPath",
        "--html=$htmlReport",
        "--self-contained-html"
    )
    if (-not $Full) {
        $pytestArgs = @("-m", $markers) + $pytestArgs
        Write-Host "[$stamp] pytest -m `"$markers`" ..."
    } else {
        Write-Host "[$stamp] 完整测试 ..."
    }

    $output = & pytest @pytestArgs 2>&1 | Out-String
    $exitCode = $LASTEXITCODE
} catch {
    $output += "`n脚本异常: $_"
    $exitCode = 1
} finally {
    $output | Set-Content -Path $logPath -Encoding UTF8

    if (-not $SkipNotify) {
        $verifySsl = Get-DotEnvValue "VERIFY_SSL"
        $insecureFlag = @()
        if ($verifySsl -eq "false") { $insecureFlag = @("--insecure") }

        if ($webhook -and (Test-Path $junitPath)) {
            $reportArgs = @(
                (Join-Path $Root "scripts\wework_test_report.py"),
                "--webhook", $webhook,
                "--junit", $junitPath,
                "--stamp", $stamp,
                "--html", $htmlReport,
                "--log", $logPath
            )
            if ($exitCode -ne 0) {
                $pdfShort = Get-Date -Format "yyyyMMdd_HHmmss"
                $pdfReport = "reports\wecom_failure_${pdfShort}.pdf"
                $reportArgs += @("--pdf-out", $pdfReport)
            }

            & python @reportArgs @insecureFlag
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "企业微信报告推送失败，尝试发送简要 Markdown ..."
                & python (Join-Path $Root "scripts\notify_wework.py") `
                    --webhook $webhook `
                    --content "### 终端接口监控测试报告`n> 时间：$stamp`n> 结论：企微推送失败，请查看 $logPath" `
                    @insecureFlag
            }
        } elseif (-not $webhook) {
            Write-Warning "未配置 WEWORK_WEBHOOK_URL，跳过企业微信"
        } else {
            Write-Warning "未生成 JUnit：$junitPath"
        }
    }
}

exit $exitCode
