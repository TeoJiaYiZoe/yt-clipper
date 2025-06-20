@echo off
echo Starting YouTube Video Clipper...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the clipper program
python clip_downloader.py

pause 