import configparser

class MyIniCfg:
    def __init__(self, sectionName):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini')
        self.section = self.cfg[sectionName]
        self.sectionName = sectionName
        
    def load_int_arg(self, name, default = 0):
        result = default
        if self.cfg.has_option(self.sectionName, name):
            result = int(self.section[name])
        return result

    def load_arg(self, name, default = ""):
        result = default
        if self.cfg.has_option(self.sectionName, name):
            result = self.section[name]
        return result