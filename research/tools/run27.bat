@echo off
REM Double-click to run the Safe check for leads_27.json. Keep this next to
REM safe-check.mjs and leads_27.json. Results go to result_27.txt (also written
REM live by the script itself, chain by chain).
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

echo Running the check...
node safe-check.mjs --batch leads_27.json --chainlist rpcs.json --out result_27.txt

echo.
echo ================================================
echo Done. Results are in result_27.txt (send it to Claude)
echo ================================================
pause
