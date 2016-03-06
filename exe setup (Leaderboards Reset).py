import sys
from cx_Freeze import setup, Executable

exe = Executable(
    script ="Leaderboards Reset.py",
    base = "Win32GUI",
    targetName="Reset Leaderboards.exe")

setup(
    name = "Reset Leaderboards",
    version = "1.0" ,
    description = "Brick Breaker Leaderboards reset",
    executables = [exe]
    )
