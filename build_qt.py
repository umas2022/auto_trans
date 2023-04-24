'''
qt项目打包脚本
除基本打包命令外删除了临时文件
'''

import os
import subprocess
from shutil import rmtree


op_name = "独立电脑配件-自助翻译"

# 执行打包命令 

subprocess.run(["pyinstaller.exe", 
                "-w", # 参数-w 不显示终端
                # "-F", # 参数-F 打包一个exe文件,太大会报错
                "-D", # 参数-D 打包多个文件，在dist中生成很多依赖文件
                "-n",op_name,  # 参数-n 或 –name 指定名称打包程序名称(默认值为脚本的基本名称)
                "-i",".\\static\\tenpula_256.ico", # 参数-i指定图标
                "--add-data","translator;translator",
                "--add-data","static;static",
                "--add-data","utils;utils",
                "--add-data","subprocess;subprocess",
                "--add-data","D:\\s-code\\self\\pctools\\venv\\Lib\\site-packages\\pykakasi\\data;pykakasi/data",
                ".\\app.py",
                "-y" # 参数-y 覆盖原有文件夹
                ], stdout=subprocess.PIPE,shell=True)

# 删除多余文件
os.remove("%s.spec" % op_name)
rmtree("./build")
