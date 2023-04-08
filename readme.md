# 电脑配件-自助翻译


### 界面
<img src="https://github.com/umas2022/auto_trans/blob/main/readme/shot.jpg" width="50%" height="50%">


### 使用说明
- 功能页: 提供两种ocr方法: tesseract(体积小)和manga-ocr(效率高,推荐)
    - tesseract可以参照下述方法安装;点击功能页截图按钮即可激活截图,完成框选后点击空格或回车键确定,c键取消,注意区分目标(竖排日文,横排日文)
    - manga-ocr可以在设置页点击安装,注意需要环境中已经安装python3.9;使用manga-ocr时需要确认功能页的剪贴板复选框已被选中,此时程序开始监听剪贴板,复制到剪贴板的日文文本会被直接翻译,使用**win+shift+s**截图并进入剪贴板的图片会被识别,无需选择目标是横排还是竖排
- 功能页: 识别到的原文内容如果有误,可以手动修改,点击[重新翻译]按钮可以对修改后的原文再次翻译
- 设置页: 没有即时更新,修改设置之后重启应用才能生效
- 设置页: 使用tesseract时截图文件会存放在缓存路径下
- 设置页: 安装manga-ocr所需时间较长,需要等到终端消失,大概需要1.2G空间
- 设置页: 启动manga-ocr后终端不能关闭
- 关于页: 没什么可关的,祝使用愉快



### 安装tesseract
- tesseract官方网站[下载](https://tesseract-ocr.github.io/tessdoc/Installation.html) 
- 安装时记得勾选 Additional language data 不然没有日文
- 建议安装到默认位置C:\Program Files\Tesseract-OCR不然要修改下面的代码


### 开发环境初始化
- 开发所用python版本为3.10和3.9(manga-ocr不支持>3.9的版本)
```
pip install -r requirements.txt
```
- 手动配置pytesseract路径  
    - 首先找到pytesseract的安装位置 pip show pytesseract
    - 例如我是d:\s-code\self\auto_trans\venv\lib\site-packages\pytesseract
    - 打开pytesseract.py,找到这句
    ```
    tesseract_cmd = 'tesseract'
    ```
    - 改为你的tesseract安装位置,比如我是
    ```
    tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ```
    - (把tesseract.exe添加到环境变量也是可以的)


### 打包
- 运行打包脚本 
```
python build_qt.py
```
- pyinstaller命令无法自动包含pykakasi的db文件,所以用add-data手动打包pykakasi\\data文件夹,如果要重新打包记得把脚本里pykakasi\\data的路径改成你自己的


### 简介
- 想在漫画ocr翻译的时候能够看到汉字的注音,所以做了这个
- cv2全屏截图后将图片无边框全屏显示,保存矩形框选区域
- tesseract-ocr工具识别图像中的文字,需要首先本地安装tesseract
- deep_translator.GoogleTranslator谷歌翻译接口
- pykakasi为汉字注音;注音仅供参考,这个库对多音字的标注效果不好
- 做好之后发现tesseract在实际使用中对竖排日文的识别效率较低,所以又做了剪贴板的监听功能,配合[manga-ocr](https://github.com/kha-white/manga-ocr)使用


### 更新
- 2023.4.7 把manga-ocr的安装和启动加入设置页里了
- 2023.4.1 增加剪贴板监听
- 2023.3.31 创建项目



