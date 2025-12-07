powershell rm -r -fo .venv -ErrorAction SilentlyContinue
powershell rm -fo uv.lock -ErrorAction SilentlyContinue
powershell rm -r -fo .idea -ErrorAction SilentlyContinue
powershell rm -r -fo __pycache__ -ErrorAction SilentlyContinue
pause
