import unittest
from weather.mgm.stations import stations
from weather.mgm.realizations import realizations


class mgm_tests(unittest.TestCase):
    def test_fetch_cities(self):

        station = stations()
        cities = station.get_cities()
        city_plaka = list(set(map(lambda x: x["ilPlaka"],cities)))

        self.assertEqual(city_plaka, list(range(1,82)))

    def test_stations_count(self):
        station = stations()
        fetched_stations = station.get_stations()
        print("Station Count:%d"%(len(fetched_stations)))
        self.assertTrue(len(fetched_stations) > 0)




if __name__ == '__main__':
    unittest.main()
