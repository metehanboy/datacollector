from configparser import ConfigParser
import psycopg2

from libs.database import db_helper
from libs.systems.directory_wizard import directory_manager as dir_manager

class dbwizard(db_helper,dir_manager):

    def __init__(self):
        self.source = "postgresql"
        dir_manager.__init__(self)
        self.__data_dir = self.assets_folder + "dbconfig" + self.sep
        self.__connection = self.__create_connection()

    def __close_db(self):
        if self.__connection is not None:
            try:
                self.__connection.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Database Error When Closing!")

    def __del__(self):
        self.__close_db()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close_db()
        print(exc_type,exc_val,exc_tb)

    def __check_error(self):
        if self.__connection is None:
            raise Exception("Veritabanı bağlantısı kurulamamış!")

    def __create_connection(self,filename="pgsql.ini",section="bulutistandb"):
        parser = ConfigParser()
        parser.read(self.__data_dir + filename)
        config = {"host":parser[section]["host"], "port":parser[section]["port"],
                  "dbname":parser[section]["dbname"], "user":parser[section]["user"],
                  "password":parser[section]["password"],"application_name":"collector_service"}
        del parser
        conn = None
        try:
            conn = psycopg2.connect(**config)

            cursor = conn.cursor()
            cursor.execute("select version()")
            cursor.close()
        except psycopg2.Error as e:
            print(e)
            return None
        return conn

    def get_db_tables(self):

        self.__check_error()

        query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'mgm';"

        cur = self.__connection.cursor()
        cur.execute(query)
        response = [r[0] for r in cur.fetchall()]
        cur.close()
        return response

    def exec(self,query):
        self.__check_error()

        cur = None
        try:
            cur = self.__connection.cursor()
            cur.execute(query)
        except Exception as e:
            print("Query çalıştırılamadı hata meydana geldi!")
            print(e)
            print("Tried Query:%s"%(query))
        finally:
            if cur != None:
                cur.close()
        return True

    def fetch(self,query):
        self.__check_error()

        cur = None
        response = None
        try:
            cur = self.__connection.cursor()
            cur.execute(query)
            response = list(cur.fetchone())
        except Exception as e:
            print("Query çalıştırılamadı hata meydana geldi!")
            print(e)
        finally:
            if cur != None:
                cur.close()
        return response

    def fetchall(self,query):
        self.__check_error()

        cur = None
        response = None
        try:
            cur = self.__connection.cursor()
            cur.execute(query)
            response = [r[0] for r in cur.fetchall()]
        except Exception as e:
            print("Query çalıştırılamadı hata meydana geldi!")
            print(e)
        finally:
            if cur != None:
                cur.close()
        return response