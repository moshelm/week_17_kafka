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
    'database': MYSQL_DATABASE
}
class Mysql_Manger():
    def get_connection(self):
        try: 
            return connection.MySQLConnection(**CONFIG_DB)
        except Exception as e:
            print(f'failed to connection {e}')

    def query(self, sql_query: str, params: tuple = None):
        conn = self.get_connection()
        res = None
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query, params or ())
                
                if cursor.with_rows:
                    res = cursor.fetchall()
                
                conn.commit()
                return res
                
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()
        finally:
            conn.close()