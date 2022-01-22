from requests import Request, Session
from urllib.parse import urlparse

from libs.systems.directory_wizard import directory_manager as dir_manager


class web_client(dir_manager):
    def __init__(self):

        dir_manager.__init__(self)
        self.__webassets = self.assets_folder + "web_config" + self.sep
        self.__cookie_folder = self.__webassets + "cookie" + self.sep
        self.create_dir(self.__webassets)
        self.create_dir(self.__cookie_folder)

        self.__session = Session()

    def __arg_parser(self,kwargs):
        header = kwargs["header"] if "header" in kwargs else None
        param = kwargs["param"] if "param" in kwargs else None
        data = kwargs["data"] if "data" in kwargs else None
        json = kwargs["json"] if "json" in kwargs else None

        return header,param,data,json

    def __chromium_headers(self,url,headers=None,referer=None):

        url_options = urlparse(url)

        with open(self.__webassets + "chrome.headers.txt","r") as fh:
            chrome_headers = fh.read()

        chrome_headers = list(filter(lambda x: x != "",map(lambda x: x.strip(),chrome_headers.strip().split("\n"))))
        chrome_headers = {x.split(":")[0]:x.split(":")[1] for x in chrome_headers}

        chrome_headers["Referer"] = url_options.hostname if referer == None else referer
        chrome_headers["Origin"] = url_options.hostname
        chrome_headers["Host"] = url_options.hostname

        if headers != None:
            for key in headers.keys():
                chrome_headers[key] = headers.get(key)

        return chrome_headers

    def get_request(self,url,**kwargs):

        header, param, data, json = self.__arg_parser(kwargs)

        if "ischrome" in kwargs:
            header = self.__chromium_headers(url, header)

        req = Request('GET', url, headers=header, params=param)
        prepared = req.prepare()
        return self.__session.send(prepared)

    def data_request(self,url,type="POST",**kwargs):

        header,param,data,json = self.__arg_parser(kwargs)
        if "ischrome" in kwargs:
            header = self.__chromium_headers(url,header)

        if json != None:
            req = Request(type,url,headers=header,json=json,params=param)
        else:
            req = Request(type,url,headers=header,data=data,params=param)

        prepared = req.prepare()
        return self.__session.send(prepared)