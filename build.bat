@echo off
echo Installing PyInstaller and dependencies...
pip install -r requirements.txt

echo Building NEXUS-100 Executable...
REM The --onefile flag packages everything into a single .exe
REM The --name flag sets the output file name
pyinstaller --onefile --name "NEXUS-100" main.py

echo Build complete! You can find the executable in the 'dist' folder.
pause
