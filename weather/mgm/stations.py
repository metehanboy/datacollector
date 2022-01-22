from weather.mgm import mgm


class stations(mgm):

    def __init__(self):
        mgm.__init__(self)

    def get_cities(self):
        path = "/web/merkezler/iller"
        cities = self.make_request(self.mgmapi + path, "GET").json()
        return sorted(cities, key=lambda x: x["ilPlaka"])

    def get_stations(self):
        cities = self.get_cities()
        data = []
        for city in cities:
            data = data + self.__stations_request_by_cityname(city["il"])
        return sorted(data, key=lambda x: x["istNo"])

    def get_districts(self):
        cities = self.get_cities()
        data = []
        for city in cities:
            data = data + self.__district_request(city["il"])
        return sorted(data,key=lambda x: x["ilPlaka"])

    def __district_request(self,city_name):
        path = "/web/merkezler/ililcesi"
        params = {"il": city_name}
        return self.make_request(self.mgmapi + path, "GET", param=params).json()
    def __stations_request_by_cityname(self,city_name):
        path = "/web/istasyonlar/ilAdDetay"
        params = {"il": city_name}

        return self.make_request(self.mgmapi + path, "GET", param=params).json()


    def auto_task(self):
        cities = self.get_cities()
        districts = self.get_districts()
        stations = self.get_stations()

        self.import_query_builder(cities,"cities")
        self.import_query_builder(districts,"districts")
        self.import_query_builder(stations,"stations")

