from configparser import ConfigParser
import os

class ConfigProcessor:

    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg")  #os.environ["PSEUDO_CONFIG_PATH"]
        self.config = ConfigParser()
        self.config.read_file(open(self.config_path))


    def get_pseudo_API(self):
        return self.config.get("miseq-config", "PSEUDONYMIZATION-API")


    def get_export_API(self):
        return self.config.get("miseq-config", "EXPORT-API")