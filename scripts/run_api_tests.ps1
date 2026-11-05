$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "已根据 .env.example 生成 .env，请修改 API_BASE_URL 后重试。"
}

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt

New-Item -ItemType Directory -Force -Path "reports" | Out-Null

pytest -m smoke --html=reports/report.html --self-contained-html @args
