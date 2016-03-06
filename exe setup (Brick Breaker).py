import sys
from cx_Freeze import setup, Executable

includesfiles = ["Assets/HighScore.txt",
                 "Assets/Computing game images/BB_Icon.bmp",
                 "Assets/Computing game images/Leaderboards.png",
                 "Assets/Computing game images/Menu image.png",
                 "Assets/Computing game images/Pause Screen.png",
                 "Assets/Computing game images/stars.jpg"]
includes = []
excludes = []
packages = []

exe = Executable(
    script ="BrickBreaker.py",
    base = "Win32GUI",
    targetName="Brick Breaker.exe",
    icon = "Assets/Computing game images/BB_Icon.ico" )

setup(
    name = "Brick Breaker",
    version = "1.0" ,
    description = "Brick Breaker Game",
    options = {'build_exe':{'excludes':excludes,
                            'packages': packages,
                            'include_files':includesfiles}},
    executables = [exe]
    )
