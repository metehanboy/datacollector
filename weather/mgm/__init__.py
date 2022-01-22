import random
from configparser import ConfigParser

from libs.systems.directory_wizard import directory_manager as dir_manager
from libs.systems.web_client import web_client

class mgm(web_client,dir_manager):

    def __init__(self):
        dir_manager.__init__(self)
        self.root = self.get_root() + "weather" + self.sep + "mgm" + self.sep

        config = ConfigParser()
        config.read(self.root + "helpers" + self.sep + "config.ini")

        self.__db_init(config)

        web_client.__init__(self)

        self.mgmapi = config["DEFAULT"]["mgm_servis"]

        self.upsert_query = "insert into {table_name} ({columns}) values {values} {constraint} do update set {excluded_lists}"


    def __db_init(self,config):
        if config["DEFAULT"]["dbtype"] == "postgresql":
            self.__postgresql_init(config)
        else:
            self.__sqlite_init(config)
    def __sqlite_init(self,config):
        from libs.database.sqlite import dbwizard
        self.db = dbwizard("mgm")

        self.__db_migrate("sqlite",self.root)
    def __postgresql_init(self,config):
        from libs.database.postgresql import dbwizard

        self.db = dbwizard()

        self.__db_migrate("postgresql",self.root)
    def __db_migrate(self,type,root):
        tables = self.db.get_db_tables()
        root = root + "helpers" + self.sep + "migrates" + self.sep + type + self.sep

        for file in self.list_directory(root):
            if file.replace(".sql","") not in tables:
                print("DB Type:%s Migrated Table:%s"%(type,file.replace(".sql","")))
                with open(root + file, "r") as fh:
                    query = fh.read()
                for q in query.split(";"):
                    if q == "":
                        continue
                    self.db.exec(q + ";")


    def __order_data_by_columns(self,row,columns):
        return [row[col] if col in row else None for col in columns]
    def __sql_values_importer(self,table_name,columns,excluded_remover,constraint,data):
        table_name = table_name if self.db.source == "sqlite" else "mgm."+table_name
        updated = "datetime('now','localtime')" if self.db.source == "sqlite" else "current_timestamp"
        excluded = columns.split(",")
        for remove in excluded_remover.split(","):
            excluded.remove(remove)
        excluded_list = ",".join(['"%s"'%i + "=EXCLUDED." + '"%s"'%i for i in excluded] + ["updated = " + updated])

        query_columns = ",".join(list(map(lambda x: '"%s"' % (x), columns.split(","))))
        constraint_str = "on conflict on constraint " if self.db.source == "postgresql" else "on conflict "
        constraint_str += constraint if self.db.source == "postgresql" else "("+",".join(map(lambda x: '"%s"'%(x),constraint.split(","))) + ")"

        for chunk in self.db.chunker(data):
            row = list(map(lambda row: list(map(lambda col: self.db.tip_belirle(col),
                                                self.__order_data_by_columns(row,columns.split(",")))),chunk))
            values = ",".join(["(%s)"%(",".join(r)) for r in row])
            tmp_query = self.upsert_query.format(table_name = table_name,
                                                 columns = query_columns,
                                                 excluded_lists = excluded_list,
                                                 values = values,
                                                 constraint = constraint_str)
            self.db.exec("BEGIN;")
            self.db.exec(tmp_query)
            self.db.exec("COMMIT;")


    def __city_importer(self,data):
        columns = "alternatifHadiseIstNo,boylam,enlem,gunlukTahminIstNo,il,ilPlaka,ilce,merkezId,oncelik,saatlikTahminIstNo,sondurumIstNo,yukseklik,aciklama,modelId,gps"
        excluded = "ilPlaka"
        constraint = "ilPlaka" if self.db.source == "sqlite" else "cities_key"
        return self.__sql_values_importer("cities",columns,excluded,constraint,data)
    def __district_importer(self,data):
        columns = "alternatifHadiseIstNo,boylam,enlem,gunlukTahminIstNo,il,ilPlaka,ilce,merkezId,oncelik,saatlikTahminIstNo,sondurumIstNo,yukseklik,aciklama,modelId,gps"
        excluded = "ilPlaka,ilce"
        constraint = "ilPlaka,ilce" if self.db.source == "sqlite" else "districts_key"
        return self.__sql_values_importer("districts", columns, excluded, constraint, data)
    def __station_importer(self,data):
        columns = "istNo,istAd,enlem,boylam,yukseklik,ilPlaka,il,ilce,BirimId,Indikator,BasincSensor,NemSensor,RuzgarSensor,SicaklikSensor,ToprakSicSensor,HaliHazirHavaSensor,OmgiGrupAdi,YagisSensor,KarSensor"
        excluded = "ilPlaka,istNo"
        constraint = "ilPlaka,istNo" if self.db.source == "sqlite" else "stations_key"
        return self.__sql_values_importer("stations", columns, excluded, constraint, data)
    def __observation_importer(self,data):
        columns = "aktuelBasinc,denizSicaklik,denizeIndirgenmisBasinc,gorus,hadiseKodu,istNo,kapalilik,karYukseklik,nem,rasatMetar,rasatSinoptik,rasatTaf,ruzgarHiz,ruzgarYon,sicaklik,veriZamani,yagis00Now,yagis10Dk,yagis12Saat,yagis1Saat,yagis24Saat,yagis6Saat,denizVeriZamani"
        excluded = "istNo,veriZamani"
        constraint = "istNo,veriZamani" if self.db.source == "sqlite" else "last_observations_key"
        return self.__sql_values_importer("last_observations", columns, excluded, constraint, data)

    def import_query_builder(self,data,table_name):
        if table_name == "cities":
            self.__city_importer(data)
        elif table_name == "districts":
            self.__district_importer(data)
        elif table_name == "stations":
            self.__station_importer(data)
        elif table_name == "last_observations":
            self.__observation_importer(data)


    def mgm_headers(self,referer = "https://mgm.gov.tr"):

        ip = '.'.join('%s'%random.randint(0, 255) for i in range(4))

        with open(self.root + "helpers" + self.sep + "mgm.headers.txt","r") as fh:
            headers = fh.read()

        headers = list(filter(lambda x: x != "", map(lambda x: x.strip(), headers.strip().split("\n"))))
        headers = {x.split(":")[0]: x.split(":")[1] for x in headers}

        headers["Origin"] = "https://mgm.gov.tr"
        headers["Host"] = "servis.mgm.gov.tr"
        headers["Referer"] = referer

        headers["X-Client-IP"] = ip
        headers["Client-IP"] = ip
        headers["HTTP_X_FORWARDED_FOR"] = ip
        headers["HTTP_X_FORWARDED_BY"] = ip
        headers["X-Forwarded-For"] = ip
        headers["X-Forwarded-By"] = ip
        headers["HTTP_X_REAL_IP"] = ip
        headers["UNTRUSTED-PROXY"] = ip
        headers["REMOTE_ADDR"] = ip

        return headers
    def make_request(self,url,type="GET",**kwargs):

        headers = self.mgm_headers()

        if type != "GET":
            return self.data_request(url, type, header=headers, **kwargs)

        return self.get_request(url, header=headers, **kwargs)