@echo off
REM === Proje dizinine geç ===
cd /d "%~dp0"

REM === Sanal ortamı aktif et ===
call .venv\Scripts\activate

REM === Projeyi modül olarak çalıştır ===
python -m controller.Login

pause
