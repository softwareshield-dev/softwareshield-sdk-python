@ECHO OFF
REM Run unit tests on Windows platform

SETLOCAL

SET PATH=%PATH%;%SDK_BIN%;%CD%
call python -m unittest -v tests.test_core.TestCoreStatic
call python -m unittest -v tests.test_core.TestCoreAPI

ENDLOCAL