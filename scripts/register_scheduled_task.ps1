# 注册 Windows 计划任务：每 15 分钟执行一次接口自动化巡检
# 需以管理员运行：右键 PowerShell -> 以管理员身份运行

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $Root "scripts\run_scheduled_api_test.ps1"
$taskName = "TerminalMonitor-ApiTest-Every15Min"

if (-not (Test-Path $runner)) {
    Write-Error "找不到脚本: $runner"
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$runner`""

# 从当前时刻起每 15 分钟重复，持续 10 年（可手动重新注册延长）
$start = Get-Date
$trigger = New-ScheduledTaskTrigger `
    -Once `
    -At $start `
    -RepetitionInterval (New-TimeSpan -Minutes 15) `
    -RepetitionDuration (New-TimeSpan -Days 3650)

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "terminal_monitor 接口自动化：每 15 分钟 pytest + 企业微信通知" `
    -Force | Out-Null

Write-Host "已注册计划任务: $taskName"
Write-Host "脚本: $runner"
Write-Host "查看: Get-ScheduledTask -TaskName '$taskName' | Get-ScheduledTaskInfo"
Write-Host "删除: Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
