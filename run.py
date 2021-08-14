from ini_config import MyIniCfg
from img_generator import ImgGenerator

def main():
    cfg = MyIniCfg("image")
    imgGenerator = ImgGenerator(cfg)
    imgGenerator.generate()

main()