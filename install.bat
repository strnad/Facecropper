@echo off
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo. installing requirements...
pip install -r requirements.txt
mkdir _INPUT
mkdir _OUTPUT
echo Now you can run the run.bat to process all photos in _INPUT folder, you will find the cropped photos in _OUTPUT folder. Enjoy! :)