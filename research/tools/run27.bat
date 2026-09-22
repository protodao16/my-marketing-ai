@echo off
REM Double-click to run the Safe check for the 27-project list (leads_27.json).
REM Keep this file next to safe-check.mjs and leads_27.json.
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo [!] Node.js is not installed. Install the "LTS" build from https://nodejs.org , then double-click again.
  echo.
  pause
  exit /b
)

echo Installing Safe address package (one time)...
call npm install @safe-global/safe-deployments

echo Downloading fresh chainlist...
curl -s https://chainlist.org/rpcs.json -o rpcs.json

echo Running the check on leads_27.json ...
node safe-check.mjs --batch leads_27.json --chainlist rpcs.json > result_27.txt 2>&1

echo.
echo ================================================
echo Done. Results are in the file: result_27.txt
echo (send that file back to Claude)
echo ================================================
echo.
type result_27.txt
pause
