from configparser import ConfigParser
import os

class ConfigProcessor:

    def __init__(self):
        self.config_path = "/home/houfek/Work/MMCI/sequencing_pipeline/data-catalogue-pseudonymisation/MiSEQ/config.cfg"  #os.environ["PSEUDO_CONFIG_PATH"]
        self.config = ConfigParser()
        self.config.read_file(open(self.config_path))


    def get_pseudo_API(self):
        return self.config.get("miseq-config", "PSEUDONYMIZATION-API")


    def get_export_API(self):
        return self.config.get("miseq-config", "EXPORT-API")