__author__ = 'tian'
from captcha.image import ImageCaptcha

#import captcha
import random

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from setting import number,alphabet,ALPHABET


def random_captcha_text(char_set=number + alphabet + ALPHABET, captcha_size=5):
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha(width=80,height=23,font_sizes=(23,26,28))


    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text)

    captcha = image.generate(captcha_text)
    #image.write(captcha_text, captcha_text + '.jpg')  # 写到文件


    captcha_image = Image.open(captcha)

    captcha_image = np.array(captcha_image)
    #print(captcha_image)
    # captcha_image = np.array(captcha)
    #
    # print(captcha_image)
    return captcha_text, captcha_image


if __name__ == '__main__':

    text, image = gen_captcha_text_and_image()

    f = plt.figure()

    plt.imshow(image)

    plt.show()
