'''
2023.3.31
漫画截图翻译
'''


import os
import subprocess
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from PIL import Image
import pytesseract  # pip install pytesseract # 需要配置pytesseract路径
from deep_translator import GoogleTranslator  # pip install deep-translator
import pykakasi  # pip install Cython # pip install pykakasi

import sys,os
script_path =os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)
from utils_logger import logger

class AutoTrans():
    '''漫画截图翻译'''

    def __init__(self, json_set={}) -> None:
        '''带*号标记为必填项'''
        try:
            # * 目标路径
            self.save_path = os.path.normpath(json_set['save_path'])
            # 日志路径
            self.path_log = os.path.normpath(json_set['path_log']) if "path_log" in json_set else ""
            self.path_log = "" if self.path_log == "." else self.path_log
            # logger.raw_logger.set_path(self.path_log)
            # * 目标语言
            self.target = json_set['target']
            # * 翻译语言
            self.translate = json_set['translate']
        except Exception as e:
            logger.error("key error: %s" % e)
            return
        # 截图文件名和路径
        self.jpg_name = "shot.jpg"
        self.jpg_path = os.path.join(self.save_path, self.jpg_name)
        # 全屏截图句柄
        self.img = ""
        # 全屏截图鼠标位置
        self.point1 = (0, 0)
        self.point2 = (0, 0)
        # 当前图片坐标
        self.pos_save = [0, 0, 0, 0]

    def startShot(self):
        '''开始截图'''
        # 获取屏幕截图
        screenshot = np.array(pyautogui.screenshot())
        # 将RGB模式的屏幕截图转换为BGR模式
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # 创建全屏窗口
        cv2.namedWindow("Screenshot", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Screenshot", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # 显示屏幕截图
        cv2.imshow("Screenshot", screenshot)

        # 等待用户选择区域
        region = cv2.selectROI("Screenshot", screenshot, fromCenter=False, showCrosshair=False)
        cv2.destroyAllWindows()

        # 获取用户选择的区域
        left, top, width, height = region

        # 截取用户选择的区域
        screenshot = screenshot[top:top + height, left:left + width]

        # 保存截图
        cv2.imwrite(self.jpg_path, screenshot)

    def get_romaji(self, text_jp) -> str:
        '''将输入的日文转换为罗马音输出'''
        text = text_jp
        kks = pykakasi.kakasi()
        result = kks.convert(text)
        sentence = ""
        for item in result:
            word = item['orig']+" (%s) "%item['hira'] if not item['orig']==  item['hira'] else item['orig']
            sentence+=word
        return sentence
    
    def get_text(self,jpg_path,target)->str:
        '''识别图片中的文字,返回去除空格和换行符的字符串'''
        try:
            img = Image.open(jpg_path)
        except:
            img = Image.open(os.path.join(jpg_path,"shot.jpg"))
        text = pytesseract.image_to_string(img, lang=target)
        text = str(text).replace(" ", "").replace("\n", "")
        return text
    
    def get_text_img(self,img,target)->str:
        '''和上面的一样,只是输入参数是已经读取好的img'''
        text = pytesseract.image_to_string(img, lang=target)
        text = str(text).replace(" ", "").replace("\n", "")
        return text
    
    def get_translate(self,text,source,translate)->str:
        '''调用谷歌接口翻译文本\n
        source = ['ja']\n
        translate = ['zh-CN']'''
        translated = GoogleTranslator(source=source, target=translate).translate(text=text)  # Chinese translation
        return translated

    def ocr_trans(self):
        '''ocr和翻译主函数'''
        try:
            text = self.get_text(self.jpg_path,self.target)
            logger.info("target: %s" % text)
            if self.target in ["jpn", "jpn_vert"]:
                translated = self.get_translate(text,"ja",self.translate)
                logger.info("romaji: %s" % self.get_romaji(text))
                logger.info("translate: %s" % translated)
            else:
                logger.error("unexpected target : %s" % self.target)
        except Exception as e:
            logger.error("translate error, %s" % e)

    def run(self):
        '''开始处理'''
        logger.info("auto trans function start ...")
        self.startShot()
        self.ocr_trans()
