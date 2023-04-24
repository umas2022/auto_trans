'''
独立进程: 启动manga-ocr
'''
import subprocess

import sys,os
script_path =os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(script_path)
print(script_path)

from utils.utils_path import abs_path

venv_path = abs_path("venv39")
vpython = abs_path("venv39\\Scripts\\python.exe")
vpip = abs_path("venv39\\Scripts\\pip.exe")
active = abs_path("venv39\\Scripts\\Activate.ps1")
manga_ocr = abs_path("venv39\\Scripts\\manga_ocr.exe")

subprocess.run(["powershell", "-Command", "&", active])
subprocess.run(["powershell", manga_ocr])
