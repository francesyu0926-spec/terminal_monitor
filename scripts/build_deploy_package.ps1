# 生成部署包（含 .env 密钥，仅用于离线部署，勿提交 Git）
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$version = Get-Date -Format "yyyyMMdd-HHmmss"
$outDir = Join-Path $Root "dist"
$stageDir = Join-Path $outDir "terminal_monitor_deploy"
$zipPath = Join-Path $outDir "terminal_monitor_deploy_$version.zip"

if (Test-Path $stageDir) { Remove-Item $stageDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stageDir | Out-Null
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$items = @(
    "api_tests",
    "scripts",
    "requirements.txt",
    "pytest.ini",
    "README.md",
    ".env.example",
    "Dockerfile",
    "docker-compose.yml",
    ".dockerignore"
)

foreach ($item in $items) {
    $src = Join-Path $Root $item
    if (-not (Test-Path $src)) {
        Write-Warning "跳过不存在的项: $item"
        continue
    }
    Copy-Item -Path $src -Destination $stageDir -Recurse -Force
}

if (Test-Path (Join-Path $Root ".env")) {
    Copy-Item (Join-Path $Root ".env") (Join-Path $stageDir ".env") -Force
    Write-Host "已包含 .env（含密钥）"
} else {
    Write-Warning "未找到 .env，部署包中无密钥文件，请在目标机器配置 .env"
}

New-Item -ItemType Directory -Force -Path (Join-Path $stageDir "reports\scheduled") | Out-Null

$deployReadme = @"
# terminal_monitor 部署包

## 环境要求
- Windows 10+
- Python 3.11+

## 首次部署
``````powershell
cd terminal_monitor_deploy
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\scripts\run_scheduled_api_test.ps1
``````

## 注册每 15 分钟定时任务（管理员）
``````powershell
.\scripts\register_scheduled_task.ps1
``````

## 敏感文件
- 本包含 `.env`（登录账号、Webhook 等），请加密存储、勿外传。
"@
Set-Content -Path (Join-Path $stageDir "DEPLOY.md") -Value $deployReadme -Encoding UTF8

if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path (Join-Path $stageDir "*") -DestinationPath $zipPath -Force
Remove-Item $stageDir -Recurse -Force

Write-Host ""
Write-Host "部署包已生成:"
Write-Host "  $zipPath"
Write-Host ("大小: {0:N2} MB" -f ((Get-Item $zipPath).Length / 1MB))
