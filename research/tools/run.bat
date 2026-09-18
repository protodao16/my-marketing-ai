@echo off
REM Double-click this file to run the Safe on-chain check.
REM It runs in its own folder, so keep safe-check.mjs and leads.json next to it.
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo [!] Node.js is not installed.
  echo     Install the "LTS" version from https://nodejs.org , then double-click this file again.
  echo.
  pause
  exit /b
)

echo Installing Safe address package (one time)...
call npm install @safe-global/safe-deployments

echo Downloading fresh chainlist...
curl -s https://chainlist.org/rpcs.json -o rpcs.json

echo Running the check...
node safe-check.mjs --batch leads.json --chainlist rpcs.json > result.txt 2>&1

echo.
echo ================================================
echo Done. Results are in the file: result.txt
echo (send that file back to Claude)
echo ================================================
echo.
type result.txt
pause
