@echo off
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Installing requirements...
pip install -r requirements.txt
mkdir _INPUT
mkdir _OUTPUT
echo Installation complete. Use run.bat to run the script.
pause
