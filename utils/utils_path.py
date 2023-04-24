'''
定位项目绝对路径
'''

import os

def abs_path(relative_path):
    """ 返回静态资源的绝对路径定位到auto_trans项目路径\n
    例如resource_path("static/tenpula_256.ico") \n
    使用相对路径打包后可能会出现找不到资源的问题,推荐使用绝对路径"""
    base_path = os.path.dirname(os.path.realpath(__file__))
    base_path = os.path.split(base_path)[0]
    return os.path.normpath(os.path.join(base_path, relative_path)) 