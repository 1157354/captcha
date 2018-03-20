#coding=utf-8
import random
import string
import sys
import math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
#from captcha.image import ImageCaptcha
 

font_path = '/Library/Fonts/Arial.ttf'
number = ['1','2','3','4','5','6','7','8','9','10']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
char_set = number+alphabet+ALPHABET



number = 5

size = (100,30)

bgcolor = (0,0,255)

fontcolor = (255,255,0)

linecolor = (105,105,105)

draw_line = True

line_number = (1,5)




#用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill = linecolor)
 
#生成验证码
def gene_code():
    for index in range(200):
        width,height = size #宽和高
        image = Image.new('RGBA',(width,height),bgcolor) #创建图片
        font = ImageFont.truetype(font_path,25) #验证码的字体
        draw = ImageDraw.Draw(image)  #创建画笔


        text = random.sample(char_set,number)
        text = ''.join(text)
        print(text)
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / number, (height - font_height) / number),text,
                font= font,fill=fontcolor) #填充字符串
        if draw_line:
            gene_line(draw,width,height)
    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    #image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
        image.save('/Users/tian/Downloads/captcha_images/'+text+'.png') #保存验证码图片
if __name__ == "__main__":
    gene_code()