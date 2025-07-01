import mysql.connector
from mysql.connector import Error
from singleton import singleton
from database.db_decorators import mysql_config
from database.mysql_conf import LOCAL_CONF

@singleton
@mysql_config(LOCAL_CONF)
class MysqlConnector:

    def connect(self):
        try:
             self.connection = mysql.connector.connect(
                host = self.cfg["host"],
                user = self.cfg["user"],
                passwd = self.cfg["password"],
                database = self.cfg["database"])
             print("connected to mysql")
        except Error as e:
            print(f"Error while connecting to MySQL '{e}'")

    def execute(self, query,params = None):
        cursor = self.connection.cursor()
        try:
            if params == None:
                cursor.execute(query)
            else:
                cursor.execute(query,params)
            if cursor.description:
                column_names = [desc[0] for desc in cursor.description]
            else:
                column_names = []
            rows = cursor.fetchall()
            result = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                result.append(row_dict)
            self.connection.commit()
            print("executed query successfully")
            return result
        except Error as e:
            print(f"Error while executing query '{e}'")    
        return None

    def close(self):
        self.connection.close()
        print("disconnected from mysql")
        self.connection = None