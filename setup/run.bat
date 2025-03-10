@echo off
chcp 65001 >nul

echo Starting development environment...

:: Start SSH agent
sc query ssh-agent | findstr /i "STOPPED" >nul
if %ERRORLEVEL% equ 0 (
    echo Starting SSH agent...
    net start ssh-agent >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to start SSH agent.
        exit /b 1
    )
)
ssh-add %USERPROFILE%\.ssh\id_ed25519 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to add SSH key to agent.
    exit /b 1
)

:: Check and start Docker
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Starting Docker...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 10 /nobreak >nul

    docker info >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to start Docker.
        exit /b 1
    )
)

:: Start container with error logging
echo Starting Docker container...
docker compose up -d --build
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to start Docker container. Check the logs above for details.
    pause
    exit /b 1
)

:: Open VSCode Dev Container
devcontainer open .
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to open VSCode Dev Container.
    exit /b 1
)

echo Development environment started successfully.
exit /b 0
