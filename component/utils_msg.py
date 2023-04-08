'''
2023.3.30
用于widget间的数据交换
'''
from PyQt6.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    '''固定为str输入,不需要输入时也要用空字符串'''
    dataChanged = pyqtSignal(str)