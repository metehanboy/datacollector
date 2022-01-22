from configparser import ConfigParser

from libs.systems.web_client import web_client
from libs.systems.directory_wizard import directory_manager as dir_manager

class base(web_client,dir_manager):

    def __init__(self):
        web_client.__init__(self)
        dir_manager.__init__(self)

        self.root = self.get_root() + "electric" + self.sep + "epias" + self.sep

    def __read_config(self):
        config = ConfigParser()
        config.read(self.root + "helpers" + self.sep + "config.ini")
