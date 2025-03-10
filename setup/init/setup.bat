@echo off
chcp 65001 >nul
echo ######################################
echo #         INITIAL SETUP START        #
echo ######################################

:: Enable SSH agent without administrator privileges
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo Checking SSH agent status...
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ssh-agent >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo WARNING: SSH agent may not be running. Attempting to start it...
    start ssh-agent >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Could not start SSH agent. You might need to start it manually.
        echo SOLUTION: Open PowerShell and run `ssh-agent` manually.
    ) else (
        echo SUCCESS: SSH agent started.
    )
) else (
    echo SUCCESS: SSH agent is already running.
)

:: Get Git user email
for /f "tokens=*" %%i in ('git config --global user.email 2^>nul') do set GIT_EMAIL=%%i
if "%GIT_EMAIL%"=="" set GIT_EMAIL=%USERNAME%@%COMPUTERNAME%
echo Git Email: %GIT_EMAIL%

:: Generate SSH key if not exists
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo Checking SSH key...
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
set SSH_KEY=%USERPROFILE%\.ssh\id_ed25519
if not exist %SSH_KEY% (
    echo SSH key not found. Generating a new one...
    ssh-keygen -t ed25519 -C "%GIT_EMAIL%" -f %SSH_KEY% -N ""
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to generate SSH key.
        pause
        exit /b 1
    )
    echo SUCCESS: SSH key created successfully.
) else (
    echo SUCCESS: SSH key already exists.
)

:: Check GitHub SSH connection
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo Testing SSH connection to GitHub...
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


:: Add SSH key to agent
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo Adding SSH key to SSH agent...
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ssh-add %SSH_KEY% >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo WARNING: Failed to add SSH key to agent. You might need to do this manually.
    echo SOLUTION: Open PowerShell and run `ssh-add %SSH_KEY%`
) else (
    echo SUCCESS: SSH key added to agent.
)

:: Check Docker status
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo Checking Docker status...
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo WARNING: Docker is not running. Please start Docker Desktop manually.
    echo SOLUTION: Open Docker Desktop and wait for it to fully start.
) else (
    echo SUCCESS: Docker is running.
)

:: Check for VSCode Dev Containers CLI
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo Checking VSCode Dev Containers CLI...
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
where devcontainer >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Dev Containers CLI is not installed.
    echo SOLUTION: Install it from: https://code.visualstudio.com/docs/devcontainers/containers#_installation
    pause
    exit /b 1
) else (
    echo SUCCESS: Dev Containers CLI is installed.
)

:: SSH 接続テストを実行
echo ooooooooooooooooooooooooooooooooooooo
ssh -o StrictHostKeyChecking=no -T git@github.com
echo ooooooooooooooooooooooooooooooooooooo

echo ######################################
echo #    INITIAL SETUP COMPLETED! 🎉     #
echo ######################################
pause
exit /b 0
