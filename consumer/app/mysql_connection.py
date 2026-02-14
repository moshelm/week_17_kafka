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
        if self.database:
            CONFIG_DB['database'] = MYSQL_DATABASE 
        return connection.MySQLConnection(**CONFIG_DB)

    def create_database(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};')
            self.database = MYSQL_DATABASE
            conn.commit()
        conn.close()
            

    def create_table_customers(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            query = f"""
            CREATE TABLE IF NOT EXISTS customers (
            customerNumber INT AUTO_INCREMENT PRIMARY KEY,
            customerName VARCHAR(255),
            contactLastName VARCHAR(255),
            contactFirstName VARCHAR(255),
            phone INT,
            addressLine1 VARCHAR(255),
            addressLine2 VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            postalCode INT,
            country VARCHAR(255),
            salesRepEmployeeNumber INT,
            creditLimit FLOAT ) 
            """
            cursor.execute(query)
            conn.commit()
        conn.close()
            

    def create_table_orders(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            query = f"""
            CREATE TABLE IF NOT EXISTS orders
            (id INT AUTO_INCREMENT PRIMARY KEY, 
            orderNumber INT,
            orderDate DATE,
            requiredDate DATE,
            shippedDate DATE,
            status VARCHAR(255),
            comments VARCHAR(255),
            customerNumber INT,
            FOREIGN KEY (customerNumber) REFERENCES customers(customerNumber) )
            """
            cursor.execute(query)
            conn.commit()
        conn.close()
            

    def insert_one(self, table_name:str,columns:list,values:list):
        flags = ', '.join(['%s'] * len(columns))
        query = f"INSERT IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({flags})"
        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(query,tuple(values))
            res = cursor.fetchall()
            for record in res:
                print(record)
            self.conn.commit()
            cursor.close()



        

