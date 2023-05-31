python -m venv venv
copy /y %~dp0\venv\Scripts\activate.bat %~dp0\venv\Scripts\activate2.bat
echo pip install -r requirement.txt >>%~dp0\venv\Scripts\activate2.bat
start %~dp0\venv\Scripts\activate2.bat