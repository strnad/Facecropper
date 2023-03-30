@echo off
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo. installing requirements...
pip install -r requirements.txt
echo Running application...
python app.py