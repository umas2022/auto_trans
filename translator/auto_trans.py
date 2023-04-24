'''
2023.3.31
漫画截图翻译
'''


import os
import cv2
import numpy as np
import pyautogui
from PIL import Image
import pytesseract  # pip install pytesseract # 需要配置pytesseract路径
from deep_translator import GoogleTranslator  # pip install deep-translator
import pykakasi  # pip install Cython # pip install pykakasi
import openai

import sys
import os
script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(script_path)
print(script_path)
from utils.utils_logger import logger


class AutoTrans():
    '''漫画截图翻译'''

    def __init__(self, save_path=".") -> None:
        '''带*号标记为必填项'''

        # 截图文件名和路径
        self.jpg_name = "shot.jpg"
        self.jpg_path = os.path.join(save_path, self.jpg_name)
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
            word = item['orig'] + " (%s) " % item['hira'] if not item['orig'] == item['hira'] else item['orig']
            sentence += word
        return sentence

    def get_text(self, jpg_path, target) -> str:
        '''识别图片中的文字,返回去除空格和换行符的字符串'''
        try:
            img = Image.open(jpg_path)
        except BaseException:
            img = Image.open(os.path.join(jpg_path, "shot.jpg"))
        return self.get_text_img(img,target)

    def get_text_img(self, img, target) -> str:
        '''和上面的一样,只是输入参数是使用Image.open读取的img'''
        try:
            text = pytesseract.image_to_string(img, lang=target)
            text = str(text).replace(" ", "").replace("\n", "")
            return text
        except Exception as err:
            err_msg = "tesseract error : %s" % err
            logger.error(err_msg)
            return err_msg

    def get_trans_google(self, text, source, target_language) -> str:
        '''调用谷歌接口翻译文本\n
        source = ['ja']\n
        target_language = ['zh-CN']'''
        translated = GoogleTranslator(source=source, target=target_language).translate(text=text)  # Chinese translation
        return translated

    def get_trans_gpt(self, text, target_language, api_key) -> str:
        '''调用chatgpt接口翻译文本\n
        translate = ['chinese']'''
        if text == "":
            return ""
        try:
            openai.api_key = api_key
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Translate '{text}' to {target_language}",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            if response.choices[0].text:
                return response.choices[0].text.strip()
            else:
                return ""
        except Exception as err:
            return str(err)


    def test(self):
        '''开始处理'''

        ocr_source = "jpn_vert" # ["jpn","jpn_vert"]
        google_source = "ja"
        google_target = "zh-CN" # ["zh-CN"]
        chatgpt_target = "chinese"
        api_key = ""

        self.startShot()

        try:
            text = self.get_text(self.jpg_path, ocr_source)
            logger.info("sourec: %s" % text)
            logger.info("romaji: %s" % self.get_romaji(text))
            logger.info("google: %s" % self.get_trans_google(text, google_source, google_target))
            logger.info("chatgpt: %s" % self.get_trans_gpt(text,chatgpt_target,api_key))
        except Exception as e:
            logger.error("translate error, %s" % e)


if __name__ == "__main__":
    AutoTrans().test()
