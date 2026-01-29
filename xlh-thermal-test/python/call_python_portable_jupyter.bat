@echo off
cls

set KEY_NAME="HKEY_CURRENT_USER\Software\xemax\python_portable"
set VALUE_NAME=pp_path
FOR /F "usebackq skip=2 tokens=1,2*" %%A IN (`REG QUERY %KEY_NAME% /v %VALUE_NAME% 2^>nul`) DO (
    set ValueName=%%A
    set ValueType=%%B
    set pp_path=%%C
)
if defined pp_path (
    echo pp_path = %pp_path%
    call "%pp_path%\start_jupyter_notebook_server.bat" "%cd%"
) else (
    echo %KEY_NAME%\%VALUE_NAME% not found
)
