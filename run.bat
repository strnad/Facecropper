@echo off
echo Choose an option:
echo 1. Run with default parameters
echo 2. Run interactively (customize parameters)
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" goto run_defaults

:interactive
echo Interactive mode: Enter your desired parameter values or press Enter to use default values.
set /p input_folder="Input folder [default=_INPUT]: "
if "%input_folder%"=="" set input_folder=_INPUT
set /p output_folder="Output folder [default=_OUTPUT]: "
if "%output_folder%"=="" set output_folder=_OUTPUT
set /p offset_x="Horizontal offset of face center [default=0.0]: "
if "%offset_x%"=="" set offset_x=0.0
set /p offset_y="Vertical offset of face center [default=-15.0]: "
if "%offset_y%"=="" set offset_y=-15.0
set /p face_percent="Size of face in the resulting photo as a percentage [default=40.0]: "
if "%face_percent%"=="" set face_percent=40.0
set /p resize="Size of the output image [default=512]: "
if "%resize%"=="" set resize=512
set /p threshold="Threshold of face detection (0-1) [default=0.5]: "
if "%threshold%"=="" set threshold=0.4
set /p output_format="Output format (jpg, png, etc.) [default=jpg]: "
if "%output_format%"=="" set output_format=jpg

call venv\Scripts\activate.bat
python app.py --input_folder %input_folder% --output_folder %output_folder% --offset_x %offset_x% --offset_y %offset_y% --face_percent %face_percent% --resize %resize% --threshold %threshold% --output_format %output_format%
pause
call venv\Scripts\deactivate.bat

:run_defaults
echo Running with default parameters...

call venv\Scripts\activate.bat
python app.py
pause
call venv\Scripts\deactivate.bat
