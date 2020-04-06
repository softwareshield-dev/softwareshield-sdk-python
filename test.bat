@ECHO OFF
REM Run unit tests on Windows platform

SETLOCAL

SET PATH=%PATH%;%SDK_BIN%;%CD%
python -m unittest 

ENDLOCAL