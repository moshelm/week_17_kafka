from mysql.connector import connection
import os 


MYSQL_USER = os.getenv('MYSQL_USER','root')
MYSQL_HOST = os.getenv('MYSQL_HOST','localhost')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE','test')
MYSQL_PORT = int(os.getenv('MYSQL_PORT','3306'))
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD','')

CONFIG_DB = {
    'user':MYSQL_USER,
    'host':MYSQL_HOST,
    'port': MYSQL_PORT,
    'password':MYSQL_PASSWORD,
}
class Mysql_Manger():
    def __init__(self):
        self.database = None


    def get_connection(self):
        try: 
            if self.database:
                CONFIG_DB['database'] = MYSQL_DATABASE 
            return connection.MySQLConnection(**CONFIG_DB)
        except Exception as e:
            print(f'failed to connection {e}')

    def query(self, query:str, params :dict):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query,params)
                res = cursor.fetchall()
                if res:  
                    for line in cursor:
                        print(line)
                conn.commit()
        except Exception as e:
            print(f'cursor failed in query {e}')
        conn.close()