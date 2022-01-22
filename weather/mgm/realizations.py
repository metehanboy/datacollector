from weather.mgm import mgm

from datetime import datetime
from dateutil import tz



class realizations(mgm):

    def __init__(self):
        mgm.__init__(self)
        self.tzlocal = tz.tzoffset('Türkiye Standart Saati', 10800)


    def auto_task(self):
        last_observations = self.istasyon_sondurumlar()
        for chunk in last_observations:
            self.import_query_builder(chunk, "last_observations")

    def istasyon_sondurumlar(self):
        plakalar = self.db.fetchall('select "ilPlaka" from cities')
        if len(plakalar) < 81:
            raise Exception("DB deki şehir bilgileri güncel değil!")
        data = {}
        for plaka in plakalar:
            data[plaka] = list(map(lambda x: self.__data_manipulate(x),
                                   self.__istasyon_sondurum_request(plaka)))
        return data

    def __toprak_sensor_request(self,istNo,tarih=datetime.now().strftime("%Y-%m-%d")):
        path = "/web/tahminler/tarimsal"
        params = {"istNo":istNo}

        return self.make_request(self.mgmapi + path, "GET", param=params).json()

    def __istasyon_sondurum_request(self,ilPlaka):
        path = "/web/sondurumlar/ilTumSondurum"
        params = {"ilPlaka": ilPlaka}

        return self.make_request(self.mgmapi + path, "GET", param=params).json()

    def __data_manipulate(self,durum):
        for key in durum:
            durum[key] = None if ((durum[key] == -9999) | (durum[key] == '-9999')) else durum[key]
            if key in "veriZamani,denizVeriZamani".split(","):
                if key == "denizVeriZamani":
                    if durum["denizSicaklik"] == None:
                        durum["denizVeriZamani"] = None
                        continue
                try:
                    durum[key] = datetime.fromisoformat(durum[key].replace("Z","+00:00")).astimezone(tz=self.tzlocal).replace(tzinfo=None)
                except:
                    durum[key] = datetime.now()
        return durum