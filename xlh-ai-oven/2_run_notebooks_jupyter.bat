if exist "%~dp0%.venv" (
  echo .
) else (
	echo =======================================================================
	echo Initialising the virtual environment
	echo Do not interrupt the process
	echo =======================================================================
	powershell uv sync
	echo =======================================================================
	echo Initialisation complete
	echo =======================================================================
)
.venv\Scripts\jupyter-lab.exe "%~dp0\notebooks"
