# Build script for WaterMarkEraser
# This script creates a standalone .exe file

Write-Host "Building WaterMarkEraser..." -ForegroundColor Cyan

# Check if PyInstaller is installed
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $pyinstaller) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# Build the executable
Write-Host "Building executable..." -ForegroundColor Green
pyinstaller --clean WaterMarkEraser.spec

# Check if build was successful
if (Test-Path "dist\WaterMarkEraser.exe") {
    Write-Host "`nBuild successful! ✓" -ForegroundColor Green
    Write-Host "Executable location: dist\WaterMarkEraser.exe" -ForegroundColor Cyan
    
    # Get file size
    $fileSize = (Get-Item "dist\WaterMarkEraser.exe").Length / 1MB
    Write-Host "File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
    
    Write-Host "`nYou can now distribute the WaterMarkEraser.exe file!" -ForegroundColor Green
} else {
    Write-Host "`nBuild failed! ✗" -ForegroundColor Red
    Write-Host "Check the output above for errors." -ForegroundColor Red
}
