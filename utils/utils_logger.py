'''设置logger'''

import logging

logger = logging.getLogger('py_demo')


# 控制台输出格式
formatter_console = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter_console)
# 控制台输出级别
logger.setLevel(level=logging.DEBUG)
logger.addHandler(stream_handler)

# # 文件输出格式
# log_path = r"./"
# time_prefix = time.strftime("%Y-%m-%d_%H.%M", time.localtime())
# log_file = os.path.join(log_path, time_prefix + '.log')
# formatter_file = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# file_handler = logging.FileHandler(log_file, encoding='utf-8')
# file_handler.setFormatter(formatter_file)
# # 文件输出级别
# file_handler.setLevel(level=logging.WARNING)
# logger.addHandler(file_handler)