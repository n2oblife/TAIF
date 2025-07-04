# Find the PID using port 11434 and kill it
$ollamaPid = (Get-NetTCPConnection -LocalPort 11434 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1).OwningProcess
if (-not $ollamaPid) {
    Write-Host "No process found using port 11434."
    exit 1
}
Write-Host "Stopping process with PID $ollamaPid using port 11434..."
Stop-Process -Id $ollamaPid -Force 