import os
import random
import backgroundgen as bg

from xml_builder import XmlBuilder
from ini_config import MyIniCfg
from text_img_generator import TextImgGenerator

from PIL import ImageDraw, Image, ImageFilter, ImageOps

class ImgGenerator:
    def __init__(self, cfg):      
        self.cfg = cfg      
        self.numberCount = cfg.load_int_arg("number_count")         
        self.width = cfg.load_int_arg("width")
        self.height = cfg.load_int_arg("height")
        self.bgGenerator = bg.BackgroundGenerator()

        destPath = cfg.load_arg('dest_path')
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        
        self.xmlbuilder =  XmlBuilder(destPath, (self.width, self.height))
        self.destPath = destPath

        cfg = MyIniCfg("text")
        self.textImgGenerator = TextImgGenerator(cfg, (self.width, self.height), self.xmlbuilder)

    def generate(self):
        cfg = self.cfg
        count = cfg.load_int_arg('image_count')

        for x in range(count):   
            print("--------------------------------------------")          
            print("Начало генерации изображения #", x + 1, "...")
            print("--------------------------------------------")

            xmlFilename = str(x + 1) + ".xml"
            imgFilename = str(x + 1) + ".jpg"

            fullXmlFilename = os.path.join(self.destPath, xmlFilename)
            fullImgFilename = os.path.join(self.destPath, imgFilename)

            self.xmlbuilder.SaveCommonData(imgFilename, fullImgFilename)
            
            text = self._generate_number(self.numberCount)             
            img = self._make_background()
            
            topTextImg, textInfo1 = self.textImgGenerator.generate_top(text)
            self._sum_images(img, topTextImg, textInfo1.get_basic_point())                        

            bottomTextImg, textInfo2 = self.textImgGenerator.generate_bottom(text)
            self._sum_images(img, bottomTextImg, textInfo2.get_basic_point())

            if (cfg.load_arg('boxes') == 'true'):
                self._draw_boxes(img, textInfo1)
                self._draw_boxes(img, textInfo2)
            
            img = self._make_blur(img, cfg.load_int_arg('blur'))            
            img.save(fullImgFilename)
            self.xmlbuilder.SaveXML(fullXmlFilename)
            
            print("--------------------------------------------")
            print("Генерация изображения #", x + 1, "завершено")
            print("--------------------------------------------")

    def _draw_boxes(self, img, ti):
        draw = ImageDraw.Draw(img)
        draw.rectangle(((ti.xMin, ti.yMin), (ti.xMax, ti.yMax)), outline="red")

        for i in range(0, len(ti.NumberBoxes)):
            box = ti.NumberBoxes[i] 
            draw.rectangle(((box[0], box[1]), (box[2], box[3])), outline="red")

    def _make_background(self):
        bgMethod = self.cfg.load_arg("method_bg")
        bgGenerator = self.bgGenerator

        if (bgMethod == 'picture'):
            img = bgGenerator.picture(self.height, self.width)
        elif (bgMethod == 'gaussian'):            
            img = bgGenerator.gaussian_noise(self.height, self.width)
        elif (bgMethod == 'quasicrystal'):
            img = bgGenerator.quasicrystal(self.height, self.width)
        else:            
            img = bgGenerator.plain_white(self.height, self.width)
        
        return img

    def _sum_images(self, img1, img2, anchor):                
        img1.paste(img2, anchor, img2)

    def _generate_number(self, count):
        result = ''        
        for x in range(count):
            result += str(random.randint(0, 9))
        return result

    def _make_blur(self, img, maxBlur):
        blur = random.randint(0, maxBlur)
        return img.filter(
            ImageFilter.GaussianBlur(
                radius=blur
            )
        )  