param (
[string]$pythonPath
)
if($pythonPath)
{
    Set-Alias pythonPath $pythonPath
}

$startDir = Get-Location

# build the python package
Set-Location $PSScriptRoot
Write-Host "Building package" -ForegroundColor Green

pythonPath -m bumpVersion
pythonPath -m build

Set-Location $startDir