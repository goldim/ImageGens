from PIL import Image,ImageFont, ImageDraw, ImageOps

im=Image.open("pictures/water.jpg")

f = ImageFont.load_default()
txt=Image.new('L', (500,50))
d = ImageDraw.Draw(txt)
d.text( (0, 0), "Someplace Near Boulder",  font=f, fill=255)
w=txt.rotate(90,  expand=1)
txt.show()

im.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (0,0),  w)
im.show()