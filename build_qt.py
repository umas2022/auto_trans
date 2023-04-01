'''
qt项目打包脚本
除基本打包命令外删除了临时文件
'''

import os
from shutil import rmtree
from shutil import copytree, copyfile


op_name = "独立电脑配件-自助翻译"

# 执行打包命令 
# 参数-w 不显示终端
# 参数-F 打包一个exe文件
# 参数-D 打包多个文件，在dist中生成很多依赖文件
# 参数-n 或 –name 指定名称打包程序名称(默认值为脚本的基本名称)

os.system("pyinstaller.exe -D -w -n  %s \
          -i .\\static\\mati_ei_256.ico\
           --add-data component;component \
           --add-data static;static \
           --add-data D:\\s-code\\self\\pctools\\venv\\Lib\\site-packages\\pykakasi\\data;pykakasi/data \
            .\\app.py" % op_name)

# 删除多余文件
os.remove("%s.spec" % op_name)
rmtree("./build")
