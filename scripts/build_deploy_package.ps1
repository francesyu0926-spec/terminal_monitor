# Deploy zip (includes .env secrets for offline use only; do not commit)
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
    "config",
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
        Write-Warning "Skip missing: $item"
        continue
    }
    Copy-Item -Path $src -Destination $stageDir -Recurse -Force
}

$envFile = Join-Path $Root ".env"
if (Test-Path $envFile) {
    Copy-Item $envFile (Join-Path $stageDir ".env") -Force
    Write-Host "Included .env"
} else {
    Write-Warning "No .env found; configure secrets on target host"
}

Get-ChildItem -Path $stageDir -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory -Force -Path (Join-Path $stageDir "reports\scheduled") | Out-Null

$deployReadme = @'
# terminal_monitor deploy package

Includes .env for offline/internal deploy only.

## Docker

```bash
docker compose up -d --build api-scheduler
docker compose logs -f api-scheduler
docker compose --profile once run --rm api-test-once
```

## Windows + scheduled task

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\scripts\run_scheduled_api_test.ps1
.\scripts\register_scheduled_task.ps1
```

Scheduled default: pytest -m smoke api_tests/testcases + WeCom notify.
'@
Set-Content -Path (Join-Path $stageDir "DEPLOY.md") -Value $deployReadme -Encoding UTF8

if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path (Join-Path $stageDir "*") -DestinationPath $zipPath -Force
Remove-Item $stageDir -Recurse -Force

$latestZip = Join-Path $outDir "terminal_monitor_deploy_latest.zip"
Copy-Item $zipPath $latestZip -Force

$sizeMb = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
Write-Host ""
Write-Host "Deploy package created:"
Write-Host "  $zipPath"
Write-Host "  $latestZip"
Write-Host "  Size: $sizeMb MB"
