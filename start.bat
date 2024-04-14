@echo off

IF NOT EXIST .venv (
    python -m venv .venv
)

.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m app.main