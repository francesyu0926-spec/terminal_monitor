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

# 对齐时钟：首次在下一个 15 分钟整点（:00/:15/:30/:45），之后每 15 分钟重复
$intervalMin = 15
$now = Get-Date
$slotMin = [math]::Floor($now.Minute / $intervalMin) * $intervalMin
$start = Get-Date -Year $now.Year -Month $now.Month -Day $now.Day -Hour $now.Hour -Minute $slotMin -Second 0
if ($start -le $now) {
    $start = $start.AddMinutes($intervalMin)
}

$trigger = New-ScheduledTaskTrigger `
    -Once `
    -At $start `
    -RepetitionInterval (New-TimeSpan -Minutes $intervalMin) `
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
Write-Host "首次执行（时钟对齐）: $($start.ToString('yyyy-MM-dd HH:mm:ss'))，之后每 ${intervalMin} 分钟"
Write-Host "脚本: $runner"
Write-Host "查看: Get-ScheduledTask -TaskName '$taskName' | Get-ScheduledTaskInfo"
Write-Host "删除: Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
