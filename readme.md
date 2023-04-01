# 自助翻译.exe

### 简介
- 想在漫画ocr翻译的时候能够看到汉字的注音,所以做了这个
- cv2全屏截图后将图片无边框全屏显示,保存矩形框选区域
- tesseract-ocr工具识别图像中的文字,需要首先本地安装tesseract
- deep_translator.GoogleTranslator谷歌翻译接口
- pykakasi为汉字注音
- 做好之后发现tesseract在实际使用中对竖排日文的识别效率较低,所以又做了剪贴板的监听功能,可以配合[manga-ocr](https://github.com/kha-white/manga-ocr)使用

### 界面
<img src="https://github.com/umas2022/auto_trans/blob/main/readme/shot.jpg" width="50%" height="50%">



### 安装tesseract
- tesseractd官方网站[下载](https://tesseract-ocr.github.io/tessdoc/Installation.html) 
- 安装时记得勾选 Additional language data 不然没有日文
- 建议安装到默认位置C:\Program Files\Tesseract-OCR不然要修改下面的代码


### 开发环境初始化
- 开发所用python版本为3.10
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


### 报错

- 报错
```
cv2.error: OpenCV(4.7.0) D:\a\opencv-python\opencv-python\opencv\modules\highgui\src\window.cpp:1272: error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntucript in function 'cvShowImage'
```
- 解决
```
pip install opencv-contrib-python
```

### 更新
- 2023.4.1 增加剪贴板监听
- 2023.3.31 创建项目



