import unittest
from weather.mgm.stations import stations
from weather.mgm.realizations import realizations


class mgm_tests(unittest.TestCase):
    def test_fetch_cities(self):

        station = stations()
        cities = station.get_cities()
        city_plaka = list(set(map(lambda x: x["ilPlaka"],cities)))

        self.assertEqual(city_plaka, list(range(1,82)),"Tüm Şehirler Geliyor")

    def test_stations_count(self):
        station = stations()
        fetched_stations = station.get_stations()

        self.assertTrue(len(fetched_stations) > 0,"istasyon verileri geliyor")

    def test_districts(self):
        station = stations()
        fetch_districts = station.get_districts()
        cities_from_districts = list(set(map(lambda x: x["ilPlaka"],fetch_districts)))

        self.assertEqual(cities_from_districts,list(range(1,82)),"Tüm ilçelerden veri geliyor.")

    def test_station_data_is_saved(self):

        station = stations()
        station.auto_task()

        cities = station.get_cities()
        fetch_districts = station.get_districts()
        fetched_stations = station.get_stations()

        x_city_count = len(cities)
        x_district_count = len(fetch_districts)
        x_station_count = len(fetched_stations)


        y_city_count = station.db.fetch("select count(*) as c from cities")[0]
        y_district_count = station.db.fetch("select count(*) as c from districts")[0]
        y_station_count = station.db.fetch("select count(*) as c from stations")[0]

        self.assertTrue((x_city_count == y_city_count) &
                        (x_district_count == y_district_count) &
                        (x_station_count == y_station_count),"Tüm kayıtlar içeriye alınmış.")






if __name__ == '__main__':
    unittest.main()
