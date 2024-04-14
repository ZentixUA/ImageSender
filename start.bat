@echo off
setlocal

REM Define the path to the virtual environment
set VENV=venv

REM Check and create virtual environment if it does not exist
if not exist "%VENV%\Scripts\python.exe" (
    python -m venv %VENV%
    echo Created virtual environment in %VENV%
) else (
    echo Virtual environment exists
)

REM Activate the virtual environment
call %VENV%\Scripts\activate

REM Install dependencies from requirements.txt
pip install -r requirements.txt

REM Run the app.main module
python -m app.main

REM Deactivate the virtual environment
deactivate

endlocal