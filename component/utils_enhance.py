'''
图片增强,文字识别前的预处理,用以提高识别准确度
网上找的几种方法效果都很差,放弃了,只对图片进行了放大,实测可以一定程度上稍微提到识别率
'''

def enhance(img):
    '''输入的img必须是使用PIL.Image格式打开的图片'''
    width, height = img.size

    # 调整图像大小并保存
    new_width = width * 10
    new_height = height * 10
    img = img.resize((new_width, new_height))

    return img