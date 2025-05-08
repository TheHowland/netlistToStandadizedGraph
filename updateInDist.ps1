param (
[string]$destination,
[string]$pythonPath
)
# Check if it ends with backslash
if (-not ($destination.EndsWith('\'))) {
    Write-Host "Path has to end with a backslash" -ForegroundColor Red
    exit 1
}

# Check if it's a valid path (file or directory)
if (-not (Test-Path $destination))
{
    Write-Host "Path is NOT valid (does not exist)" -ForegroundColor Red
    exit 1
}

$startDir = Get-Location

Set-Location $PSScriptRoot
$oldPackages = Get-ChildItem -Path $destination -Filter "*generalizenetlistdrawing*" -Recurse
foreach($item in $oldPackages){
    $path = [string]::Concat($destination, $item)
    Remove-Item -Path $path
    Write-Output ([string]::Concat("Removed: ", $path))
}

try{
    $newPackage = Get-ChildItem -Path "dist" -Filter "*.whl" -File | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1
}
catch {
    Write-Host "couldn't find new package in .\dist" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Set-Location $startDir
    return
}


try{
    Copy-Item -Path ([string]::Concat("dist\", $newPackage)) -Destination $destination
}
catch {
    Write-Host "could not copy new package" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Set-Location $startDir
    return
}
Write-Output "Copied $newPackage to: $destination"


Write-Host "Successfully updated generalizeNetlistDrawing package in Pyodide distribution" -ForegroundColor Green
& ([string]::Concat($pythonPath, "Scripts\Activate.ps1"))
& ([string]::Concat($pythonPath, "Scripts\pip.exe")) install ([string]::Concat("dist\", $newPackage))

Set-Location $startDir
Write-Host "Successfully installed $newPackage in virtual venv" -ForegroundColor Green