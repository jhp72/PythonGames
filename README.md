# PythonGames
Python Game Projects

# Python version
3.8.2 권장/ 
3.7.3 에서 pygame설치 후 pyCharm IDE에서 확인함

# Pyinstaller
pyinstaller  -w --add-data '.\gui_basic\img1.png;gui_basic' --add-data '.\gui_basic\img2.png;gui_basic' -F .\gui_basic\main.py

# Pyinstaller add folder with images in exe file
link: https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file
 => reference:
=======================================================

import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

========================================================
