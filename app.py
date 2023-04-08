'''
2023.3.31
自助翻译qt主窗体
'''
import sys
import os
import json
import pyperclip
import threading
import subprocess
from PIL import Image
from PyQt6.QtGui import QIcon, QFont,QDesktopServices
from PyQt6.QtCore import Qt,QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QGroupBox,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QLabel,
    QLineEdit,
    QCheckBox
)

from component.auto_trans import AutoTrans
from component.utils_logger import logger
from component.utils_path import abs_path
from component.utils_enhance import enhance
from component.utils_msg import Communicate


global gbconfig
# 加载设置
with open(abs_path("component/config.json"), "r", encoding="utf-8") as conf_file:
    gbconfig = json.load(conf_file)


class MainWindow(QMainWindow):
    '''主窗体'''

    def __init__(self):
        super(MainWindow, self).__init__()

        # 窗口名/大小/图标/布局
        self.setWindowTitle("独立电脑配件-自助翻译")
        layout_main = QVBoxLayout()
        self.setWindowIcon(QIcon(abs_path("static/mati_ei_256.ico")))

        # 创建 QTabWidget
        tab_widget = QTabWidget()
        layout_main.addWidget(tab_widget)
        # 将标签页添加到 QTabWidget 中
        tab_widget.addTab(PageFunction(), '功能')
        tab_widget.addTab(PageSettings(), '设置')
        tab_widget.addTab(PageInfo(), '关于')

        # 主体布局
        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

    def closeEvent(self, event):
        '''重写,在窗口关闭时执行的代码'''
        print("Window is closing...")
        # 关闭剪贴板监听的循环回调,否则Thread不会随着主进程的结束自动结束
        gbconfig["cblisten"] = False
        event.accept()


class PageFunction(QWidget):
    '''功能标签页'''

    def __init__(self) -> None:
        super().__init__()

        self.text = {
            # 原文
            "raw": "",
            # 注音
            "romaji": "",
            # 翻译
            "translated": ""
        }

        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 10, 0, 0)
        layout_main.setSpacing(5)

        # 第一行下拉框/两个按钮/复选框
        layout_line = QHBoxLayout()
        groupbox = QGroupBox("控制")
        layout_main.addWidget(groupbox)
        groupbox.setLayout(layout_line)

        # 第一行: 标签
        label = QLabel("剪贴板:")
        layout_line.addWidget(label)
        # 第一行: 复选框
        checkb = QCheckBox()
        if gbconfig["cblisten"]:
            checkb.setCheckState(Qt.CheckState.Checked)
        layout_line.addWidget(checkb)

        def checkb_change():
            gbconfig["cblisten"] = checkb.isChecked()
            if gbconfig["cblisten"]:
                listen_th = threading.Timer(1, self.listen_clipboard)
                listen_th.start()
        checkb.stateChanged.connect(checkb_change)

        # 第一行: 标签
        label = QLabel("目标:")
        layout_line.addWidget(label)
        # 第一行: 下拉框: 选择语言
        cbox = QComboBox()
        cbox.setFixedWidth(120)
        cbox.addItems([i['label'] for i in gbconfig["__target"]["options"]])
        cbox.currentIndexChanged.connect(lambda index: self.on_combobox_changed(index))
        layout_line.addWidget(cbox)
        # 设置初值
        for index, option in enumerate(gbconfig["__target"]["options"]):
            if option["value"] == gbconfig["target"]:
                cbox.setCurrentIndex(index)

        # 第一行: 弹簧
        layout_line.addStretch()

        # 第一行: 按钮: 截图
        btn_start = QPushButton("截图")
        btn_start.clicked.connect(self.on_click_start)
        layout_line.addWidget(btn_start)

        # 第一行: 按钮: 重新翻译
        btn_new = QPushButton("重新翻译")
        btn_new.clicked.connect(self.on_click_new)
        layout_line.addWidget(btn_new)

        # 文本区: 原文
        layout_line = QHBoxLayout()
        groupbox = QGroupBox("原文")
        layout_main.addWidget(groupbox)
        groupbox.setLayout(layout_line)

        self.raw_box = QTextEdit()
        self.raw_box.setMaximumHeight(100)
        self.raw_box.setMinimumWidth(400)
        self.raw_box.setFontPointSize(int(gbconfig["fontsize"]))
        self.raw_box.setPlaceholderText("这里显示原文")
        self.raw_box.textChanged.connect(self.on_text_change)
        layout_line.addWidget(self.raw_box)

        # 文本区: 注音
        layout_line = QHBoxLayout()
        groupbox = QGroupBox("注音")
        layout_main.addWidget(groupbox)
        groupbox.setLayout(layout_line)

        self.roma_box = QTextEdit()
        self.roma_box.setMaximumHeight(100)
        self.roma_box.setMinimumWidth(400)
        self.roma_box.setFontPointSize(int(gbconfig["fontsize"]))
        self.roma_box.setPlaceholderText("这里显示注音")
        layout_line.addWidget(self.roma_box)

        # 文本区: 翻译
        layout_line = QHBoxLayout()
        groupbox = QGroupBox("译文")
        layout_main.addWidget(groupbox)
        groupbox.setLayout(layout_line)

        self.trans_box = QTextEdit()
        self.trans_box.setMaximumHeight(100)
        self.trans_box.setMinimumWidth(400)
        self.trans_box.setFontPointSize(int(gbconfig["fontsize"]))
        self.trans_box.setPlaceholderText("这里显示译文")
        layout_line.addWidget(self.trans_box)

        # 主体布局
        self.setLayout(layout_main)

        # 文本框监听
        self.msg_box = Communicate()
        self.msg_box.dataChanged.connect(self.on_box_changed)

        # 剪贴板监听
        self.msg_cb = Communicate()
        self.msg_cb.dataChanged.connect(self.on_clipboard_changed)
        self.old_clipboard = pyperclip.paste()
        if gbconfig["cblisten"]:
            listen_th = threading.Timer(1, self.listen_clipboard)
            listen_th.start()

    def listen_clipboard(self):
        '''定时器触发,监听剪贴板'''
        new_clipboard = pyperclip.paste()
        if new_clipboard != self.old_clipboard:
            self.old_clipboard = new_clipboard
            self.msg_cb.dataChanged.emit(new_clipboard)
        # 循环回调
        if gbconfig["cblisten"]:
            call_self = threading.Timer(1, self.listen_clipboard)
            call_self.start()

    def on_clipboard_changed(self, new_clipboard):
        '''剪贴板改变触发'''
        ats = AutoTrans(gbconfig)
        self.text["raw"] = new_clipboard
        self.raw_box.setText(self.text["raw"])
        # 更新原文框
        def new_raw():
            self.msg_box.dataChanged.emit("")
        # 更新注音框
        def new_romaji():
            self.text["romaji"] = ats.get_romaji(self.text["raw"])
            self.msg_box.dataChanged.emit("")
        # 更新翻译框
        def new_trans():
            self.text["translated"] = ats.get_trans_google(self.text["raw"], gbconfig["source"], gbconfig["translate"])
            self.msg_box.dataChanged.emit("")
        th_raw = threading.Thread(target=new_raw)
        th_raw.start()
        th_romaji = threading.Thread(target=new_romaji)
        th_romaji.start()
        th_trans = threading.Thread(target=new_trans)
        th_trans.start()

    def on_box_changed(self):
        '''函数触发,刷新三个文本框的显示'''
        self.raw_box.setText(self.text["raw"])
        self.roma_box.setText(self.text["romaji"])
        self.trans_box.setText(self.text["translated"])


    def on_combobox_changed(self, index):
        '''下拉框: 选择语言'''
        if index == 0:
            gbconfig["target"] = "jpn_vert"
        elif index == 1:
            gbconfig["target"] = "jpn"

    def on_click_start(self):
        '''按钮: 启动截图'''
        ats = AutoTrans(gbconfig)
        ats.startShot()
        # 更新原文框
        def new_raw():
            self.msg_box.dataChanged.emit("")
        # 更新注音框
        def new_romaji():
            self.text["romaji"] = ats.get_romaji(self.text["raw"])
            self.msg_box.dataChanged.emit("")
        # 更新翻译框
        def new_trans():
            self.text["translated"] = ats.get_trans_google(self.text["raw"], gbconfig["source"], gbconfig["translate"])
            self.msg_box.dataChanged.emit("")
        try:
            img_path = os.path.join(gbconfig["save_path"], "shot.jpg")
            img_en_path = os.path.join(gbconfig["save_path"], "shot_en.jpg")
            img = Image.open(img_path)
            img_en = enhance(img)
            img_en.save(img_en_path)
            self.text["raw"] = ats.get_text_img(img, gbconfig["target"])
            th_raw = threading.Thread(target=new_raw)
            th_raw.start()
            th_romaji = threading.Thread(target=new_romaji)
            th_romaji.start()
            th_trans = threading.Thread(target=new_trans)
            th_trans.start()
        except Exception as err:
            logger.error("img save error : %s" % err)
            self.raw_box.setText("缓存路径不存在 ...")

        # 识别失败
        if self.text["raw"] == "":
            self.raw_box.setText("识别失败 ...")

    def on_click_new(self):
        '''按钮: 重新翻译'''
        ats = AutoTrans(gbconfig)
        self.text["romaji"] = ats.get_romaji(self.text["raw"])
        self.roma_box.setText(self.text["romaji"])
        self.text["translated"] = ats.get_trans_google(self.text["raw"], gbconfig["source"], gbconfig["translate"])
        self.trans_box.setText(self.text["translated"])

    def on_text_change(self):
        '''文本框: 原文'''
        self.text["raw"] = self.raw_box.toPlainText()


class PageSettings(QWidget):
    '''设置标签页'''

    def __init__(self) -> None:
        super().__init__()

        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(10, 10, 10, 10)
        layout_main.setSpacing(5)

        for key in gbconfig:
            if not key[0] == "_":
                continue
            set_item = gbconfig[key]
            set_value = gbconfig[key[2:]]

            # 设置QComboBox下拉框
            if set_item["type"] == "select":
                new_line = QHBoxLayout()
                # 标签
                label = QLabel(set_item['label'])
                label.setFixedWidth(100)
                new_line.addWidget(label)
                # 下拉框
                cbox = QComboBox()
                cbox.addItems([i['label'] for i in set_item['options']])
                cbox.currentIndexChanged.connect(lambda index, key=key: self.on_combobox_changed(index, key))
                new_line.addWidget(cbox)
                # 设置初值
                for index, option in enumerate(set_item["options"]):
                    if option["value"] == set_value:
                        cbox.setCurrentIndex(index)
                # 布局
                layout_main.addLayout(new_line)

            # 设置QLineEdit输入框
            elif set_item["type"] == "input":
                new_line = QHBoxLayout()
                # 标签
                label = QLabel(set_item['label'])
                label.setFixedWidth(100)
                new_line.addWidget(label)
                # 输入框
                txtl = QLineEdit()
                placeholder = set_item['placeholder'] if "placeholder" in set_item else "请输入 ..."
                txtl.setPlaceholderText(placeholder)
                txtl.textChanged.connect(lambda text, key=key: self.on_lineedit_changed(text, key))
                txtl.setText(str(set_value))
                # 布局
                new_line.addWidget(txtl)
                layout_main.addLayout(new_line)

            # 设置QCheckBox复选框
            elif set_item["type"] == "switch":
                new_line = QHBoxLayout()
                # 标签
                label = QLabel(set_item['label'])
                label.setFixedWidth(100)
                new_line.addWidget(label)
                # 复选框
                checkb = QCheckBox()
                if set_value:
                    checkb.setCheckState(Qt.CheckState.Checked)
                new_line.addWidget(checkb)
                checkb.stateChanged.connect(lambda state, key=key: self.on_checkbox_changed(state, key))
                # 布局
                new_line.addWidget(txtl)
                layout_main.addLayout(new_line)

            # 设置QPushButton按钮
            elif set_item["type"] == "button":
                new_line = QHBoxLayout()
                # 标签
                label = QLabel(set_item['label'])
                label.setFixedWidth(100)
                new_line.addWidget(label)
                # 按钮
                btn = QPushButton(set_item['label_button'])
                called_func = getattr(self, set_value)
                btn.clicked.connect(called_func)
                # 布局
                new_line.addWidget(btn)
                layout_main.addLayout(new_line)

        # 主体布局
        layout_main.addStretch()
        self.setLayout(layout_main)

    def on_combobox_changed(self, index, __key):
        '''下拉框被改变'''
        key = __key[2:]
        gbconfig[key] = gbconfig[__key]["options"][index]["value"]
        with open(abs_path("component/config.json"), "w", encoding="utf-8") as conf_file:
            conf_file.write(json.dumps(gbconfig, ensure_ascii=False))

    def on_lineedit_changed(self, text, __key):
        '''输入框被改变'''
        key = __key[2:]
        gbconfig[key] = text
        with open(abs_path("component/config.json"), "w", encoding="utf-8") as conf_file:
            conf_file.write(json.dumps(gbconfig, ensure_ascii=False))

    def on_checkbox_changed(self, state, __key):
        '''复选框被改变'''
        key = __key[2:]
        gbconfig[key] = True if state else False
        with open(abs_path("component/config.json"), "w", encoding="utf-8") as conf_file:
            conf_file.write(json.dumps(gbconfig, ensure_ascii=False))

    def btn_manga_ocr_install(self):
        '''按钮:安装manga-ocr,使用threading避免程序卡死'''
        install_script = abs_path("component/sp_manga_ocr_install.py")
        def go():
            subprocess.run(["python", install_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        go_th = threading.Thread(target=go)
        go_th.start()

    def btn_manga_ocr_start(self):
        '''按钮:启动manga-ocr,使用threading避免程序卡死'''
        install_script = abs_path("component/sp_manga_ocr_start.py")
        def go():
            subprocess.run(["python", install_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
        go_th = threading.Thread(target=go)
        go_th.start()


class PageInfo(QWidget):
    '''关于标签页'''

    def __init__(self) -> None:
        super().__init__()

        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(10, 10, 10, 10)
        layout_main.setSpacing(5)

        info_text = [
            "祝使用愉快",
            "by:umas",
            "2023.4.1"
        ]

        font = QFont()
        font.setPointSize(10)

        # 批量添加标签
        for item in info_text:
            label = QLabel(item)
            label.setWordWrap(True)
            label.setFont(font)
            layout_main.addWidget(label)

        # 链接
        url = QLabel("Visit <a href='https://github.com/umas2022/auto_trans'>Github</a>")
        url.setOpenExternalLinks(True)
        url.setFont(font)
        layout_main.addWidget(url)
        
        # 主体布局
        layout_main.addStretch()
        self.setLayout(layout_main)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
