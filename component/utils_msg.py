'''
2023.3.30
用于widget间的数据交换
'''
from PyQt6.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    dataChanged = pyqtSignal(str)