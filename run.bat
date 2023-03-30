@echo off
call venv\Scripts\activate.bat
python app.py _INPUT _OUTPUT
call venv\Scripts\deactivate.bat
