'''
独立进程: 安装manga-ocr
1. 安装虚拟环境工具virtualenv
2. 在项目目录下创建虚拟环境venv39
3. 使用powershell激活虚拟环境
4. 安装manga-ocr

注意:
    1. 机器必须安装python3.9
'''

import subprocess
from utils_path import abs_path

venv_path = abs_path("venv39")
vpython = abs_path("venv39\\Scripts\\python.exe")
vpip = abs_path("venv39\\Scripts\\pip.exe")
active = abs_path("venv39\\Scripts\\Activate.ps1")

subprocess.run("pip install virtualenv" )
subprocess.run("virtualenv -p python3.9 %s" % venv_path)
subprocess.run(["powershell", "-Command", "&", active])
subprocess.run("%s install manga-ocr" % vpip)
