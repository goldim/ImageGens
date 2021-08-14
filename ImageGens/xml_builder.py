import xml.etree.ElementTree as ET

class XmlBuilder:
    def __init__(self, destPath, resolution):
        self.root = ET.Element("annotation")
        self.destPath = destPath
        self.width = resolution[0]
        self.height = resolution[1]

    def SaveCommonData(self, filename, fullpath):
        root = self.root
        ET.SubElement(root, "folder").text = self.destPath
        ET.SubElement(root, "filename").text = filename
        ET.SubElement(root, "path").text = fullpath
        sourceXmlElement = ET.SubElement(root, "source")
        ET.SubElement(sourceXmlElement, "database").text = "Unknown"

        sizeXmlElement = ET.SubElement(root, "size")
        ET.SubElement(sizeXmlElement, "width").text = str(self.width)
        ET.SubElement(sizeXmlElement, "height").text = str(self.height)
        ET.SubElement(sizeXmlElement, "depth").text = str(3)

        ET.SubElement(root, "segmented").text = str(0)

    def SavePointCoord(self, i, xmin, xmax, ymin, ymax):
        el = ET.SubElement(self.root, "object")               
        ET.SubElement(el, "name").text = "num_" + i
        bndboxXmlElement = ET.SubElement(el, "bndbox")
        ET.SubElement(bndboxXmlElement, "xmin").text = str(xmin)
        ET.SubElement(bndboxXmlElement, "ymin").text = str(ymin)
        ET.SubElement(bndboxXmlElement, "xmax").text = str(xmax)
        ET.SubElement(bndboxXmlElement, "ymax").text = str(ymax)
        print("Сохранение цифры '", i, "' с координатами xmin, xmax, ymin, ymax: ", xmin, xmax, ymin, ymax)
    
    def SaveNumberCoords(self, xmin, xmax, ymin, ymax):
        objectXmlElement = ET.SubElement(self.root, "object")
        ET.SubElement(objectXmlElement, "name").text = "inv_num"
        bndboxXmlElement = ET.SubElement(objectXmlElement, "bndbox")
        ET.SubElement(bndboxXmlElement, "xmin").text = str(xmin)
        ET.SubElement(bndboxXmlElement, "ymin").text = str(ymin)
        ET.SubElement(bndboxXmlElement, "xmax").text = str(xmax)
        ET.SubElement(bndboxXmlElement, "ymax").text = str(ymax)
        print("Сохранение номера с координатами xmin, xmax, ymin, ymax: ", xmin, xmax, ymin, ymax)

    def SaveXML(self, filename):
        tree = ET.ElementTree(self.root)           
        tree.write(filename, xml_declaration=True, encoding='utf-8') 