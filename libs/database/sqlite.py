import sqlite3

from libs.database import db_helper
from libs.systems.directory_wizard import directory_manager as dir_manager


class dbwizard(db_helper,dir_manager):

    def __init__(self,dbname="localdata"):
        self.source = "sqlite"
        dir_manager.__init__(self)
        self.__datadir = self.assets_folder + "local_db" + self.sep
        self.create_dir(self.__datadir)

        self.__connection = self.__create_connection(dbname)

    def __close_db(self):
        if self.__connection is not None:
            try:
                self.__connection.close()
            except Exception as error:
                print(error)
                print("Database Error When Closing!")

    def __del__(self):
        self.__close_db()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close_db()
        print(exc_type,exc_val,exc_tb)


    def __check_error(self):
        if self.__connection is None:
            raise Exception("Veritabanı bağlantısı kurulamamış!")

    def __create_connection(self,dbname):

        conn = None
        try:
            conn = sqlite3.connect(self.__datadir + dbname + ".db")
            cursor = conn.cursor()
            cursor.execute("select * from sqlite_master")
            cursor.close()
        except sqlite3.Error as e:
            print(e)

        return conn

    def get_db_tables(self):

        self.__check_error()

        query = "SELECT name FROM sqlite_master WHERE type='table';"

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