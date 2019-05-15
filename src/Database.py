import pymysql


class MySQL:
    def __init__(self):
        self.db = pymysql.connect("120.77.38.66", "distributed", "20190501", "chat")

    def modify(self, query, *args):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, args)

            self.db.commit()
        finally:
            self.db.close()

    def select(self, query):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        finally:
            self.db.close()
            return result

    def connect(self):
        self.db = pymysql.connect("120.77.38.66", "distributed", "20190501", "chat")
