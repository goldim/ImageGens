import os
import random
from img_text_info import ImgTextInfo
from PIL import ImageDraw, Image

class TextImgGenerator: 
    def __init__(self, cfg, resolution, xmlbuilder):    
        self.xmlbuilder = xmlbuilder    
        self.cfg = cfg     
        self.imgW = resolution[0]
        self.imgH = resolution[1]       

    def random_between(self, minName, maxName):
        return random.randint(self.cfg.load_int_arg(minName), self.cfg.load_int_arg(maxName))   

    def get_fontpath(self, fontPath=""):        
        result = fontPath
        
        if (fontPath == "" or not os.path.isfile(fontPath)):            
            fontdir = "fonts"
            result = os.path.join(fontdir, random.choice([x for x in os.listdir(fontdir) if os.path.isfile(os.path.join("fonts", x))]))     

        return result

    def get_color(self, hexcode = ""):
        if (hexcode == ""):
            fontColor = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))     
        else:
            r,g,b = bytes.fromhex(hexcode)
            fontColor = (r,g,b)
        return fontColor

    def generate_top(self, text):
        return self.generate(text, 0, self.imgW, 0, int(self.imgH / 3 * 2), 'font_top_size_min', 'font_top_size_max', 'font_top', 'font_top_color')
        

    def generate_bottom(self, text):
        return self.generate(text, 0, self.imgW, int(self.imgH / 3 * 2), self.imgH, 'font_bottom_size_min', 'font_bottom_size_max', 'font_bottom', 'font_bottom_color')

    def generate(self, text, beginW, endW, beginH, endH, fontNameMin, fontNameMax, fontPath, fontColor):        
        textInfo = ImgTextInfo(text)

        angle = self.random_between('angle_min', 'angle_max')
        textInfo.set_angle(angle)
        fontSize = self.random_between(fontNameMin, fontNameMax)
        fontFullPath = self.get_fontpath(self.cfg.load_arg(fontPath))         
        textInfo.make_font(fontFullPath, fontSize)
        textInfo.calc_coords(beginW, endW, beginH, endH)

        textImg = Image.new('RGBA', (textInfo.textW, textInfo.textH))
        draw = ImageDraw.Draw(textImg)
        draw.text((0,0), text, font = textInfo.font, fill = self.get_color(self.cfg.load_arg(fontColor)))
        
        textImg = textImg.rotate(angle, expand=1)                        
        self.WriteDataToXmlFile(self.xmlbuilder, textInfo)
        
        return textImg, textInfo
    
    def WriteDataToXmlFile(self, xmlbuilder, ti):
        xmlbuilder.SaveNumberCoords(ti.xMin, ti.xMax, ti.yMin, ti.yMax)

        for i in range(0, len(ti.NumberBoxes)):
            box = ti.NumberBoxes[i] 
            xmlbuilder.SavePointCoord(ti.text[i], box[0], box[1], box[2], box[3])
            