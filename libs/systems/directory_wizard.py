import os

class directory_manager:

    def __init__(self):
        self.__root = self.__detect_root()
        self.sep = os.sep
        self.assets_folder = self.__root + "assets" + self.sep

    def get_root(self):
        return self.__root

    def __detect_root(self):
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + os.sep

    def create_dir(self, path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self.create_dir(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)

    def file_exists(self, file):
        if os.path.exists(file):
            return file
        return False

    def list_directory(self,path):
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]