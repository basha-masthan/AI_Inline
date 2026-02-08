@echo off
setlocal
cd /d "%~dp0"
title GitHub AI Assistant

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python from https://python.org
    pause
    exit /b
)

:: Run the assistant (Python now handles the setup if .env is missing)
python ai_assistant.py

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Application closed.
    pause
)
