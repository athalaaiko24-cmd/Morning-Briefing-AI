@echo off
title Morning Briefing AI
color 0A

echo.
echo  ================================
echo    MORNING BRIEFING AI
echo  ================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python tidak ditemukan!
    echo  Download Python di: https://python.org
    pause
    exit /b
)

echo  Mengecek library yang dibutuhkan...
pip show google-genai >nul 2>&1
if errorlevel 1 (
    echo  Installing google-genai...
    pip install google-genai -q
)

echo  Library siap!
echo.

python "%~dp0briefing.py"
if errorlevel 1 (
    echo.
    echo [ERROR] Ada masalah saat menjalankan script.
    pause
)
