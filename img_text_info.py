import math
import random
from PIL import ImageFont, ImageDraw, Image, ImageFilter

def lineEq(x, x1, y1, x2, y2):
    return int(((x - x1) * (y2 - y1)) / (x2 - x1) + y1)

def rotateCoordCounterClockwise(x0, y0, x, y, rad): 
    xr = int((x - x0) * math.cos(rad) - (y - y0) * math.sin(rad)   + x0)
    yr = int((x - x0) * math.sin(rad) + (y - y0) * math.cos(rad)   + y0)
    return xr, yr

class ImgTextInfo:
    def __init__(self, text):
        self.angle = 0
        self.font = None
        self.textW = 0
        self.textH = 0
        self.rect = ((0,0), (0,0), (0,0), (0,0))
        self.text = text

        self.xMin = 0
        self.yMin = 0
        self.xMax = 0
        self.yMax = 0 
        pass

    def make_font(self, name, size):        
        self.font = ImageFont.truetype(name, size)
        self.textW, self.textH = self.font.getsize(self.text)

    def set_angle(self, angle):
        self.angle = angle

    def get_basic_point(self):
        # return self.rect[0]
        if (self.angle >= 0):
            print(self.rect[0][0], self.rect[0][1] - int(math.sin(math.radians(self.angle)) * self.textW))
            return (self.rect[0][0], self.rect[0][1] - int(math.sin(math.radians(self.angle)) * self.textW))
        else:
            return (self.rect[0][0] - int(math.sin(math.radians(self.angle)) * self.textH), self.rect[0][1])

    def calc_coords(self, beginW, endW, beginH, endH):         
        rads = math.radians(self.angle)  

        x1 = 0
        y1 = 0

        if (self.angle >= 0):                         
            topH = int(self.textW * math.sin(rads))
            rightW =  int(self.textW * math.cos(rads) + self.textH * math.sin(rads))
            bottomH = int(self.textH * math.cos(rads))
            x1 = random.randint(beginW, endW - rightW)
            y1 = random.randint(beginH + topH, endH - bottomH)  
        else:
            leftW = abs(int(self.textH * math.sin(rads)))
            rightW = abs(int(self.textW * math.cos(rads)))
            bottomH = int(abs(self.textW * math.sin(rads)) + abs(self.textH * math.cos(rads)))
            x1 = random.randint(beginW + leftW, endW - rightW)
            y1 = random.randint(beginH, endH - bottomH)  

        print("calc", x1,y1)
        x3 = x1 + self.textW
        y3 = y1 + self.textH

        x2 = x1
        y2 = y3

        x4 = x3
        y4 = y1

        rads = math.radians(-self.angle)
        x2rot, y2rot = rotateCoordCounterClockwise(x1, y1, x2, y2, rads)
        x3rot, y3rot = rotateCoordCounterClockwise(x1, y1, x3, y3, rads)
        x4rot, y4rot = rotateCoordCounterClockwise(x1, y1, x4, y4, rads)  

        xMin = min(x1, x2rot, x3rot, x4rot)
        yMin = min(y1, y2rot, y3rot, y4rot)
        xMax = max(x1, x2rot, x3rot, x4rot)
        yMax = max(y1, y2rot, y3rot, y4rot)

        self.rect = ((x1,y1), (x2rot, y2rot), (x3rot, y3rot), (x4rot, y4rot))        

        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax 

        self._calc_coords_of_each_number()

    def _calc_coords_of_each_number(self):
        x1next = self.rect[0][0]
        y1next = self.rect[0][1]
        x2next = self.rect[1][0]
        y2next = self.rect[1][1]        

        numberW = int(self.textW / len(self.text))
                
        x3next = self.rect[1][0] + numberW
        y3next = lineEq(x3next, self.rect[1][0], self.rect[1][1], self.rect[2][0], self.rect[2][1])

        x4next = self.rect[0][0] + numberW
        y4next = lineEq(x4next, self.rect[0][0], self.rect[0][1], self.rect[3][0], self.rect[0][1])

        result = []

        for i in range(0, len(self.text)): 
            xmin = min(x1next, x2next, x3next, x4next)
            ymin = min(y1next, y2next, y3next, y4next)
            xmax = max(x1next, x2next, x3next, x4next)
            ymax = max(y1next, y2next, y3next, y4next)
            result.append([xmin, ymin, xmax, ymax])

            x1next = x4next
            y1next = y4next
            x2next = x3next
            y2next = y3next
            
            x3next = x2next + numberW
            y3next = lineEq(x3next, self.rect[1][0], self.rect[1][1], self.rect[2][0], self.rect[2][1])            
            x4next = x1next + numberW
            y4next = lineEq(x4next, self.rect[0][0], self.rect[0][1], self.rect[3][0], self.rect[3][1])

        self.NumberBoxes = result