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
    # 'database': MYSQL_DATABASE
}
conn = connection.MySQLConnection(**CONFIG_DB)
cursor = conn.cursor()

def create_database():
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};')
        conn.commit()
        cursor.close()
        

def create_table_costumers():
    with conn.cursor() as cursor:
        query = f"""USE {MYSQL_DATABASE};
        CREATE TABLE IF NOT EXISTS costumers (
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
        cursor.close()
        

def create_table_orders():
    with conn.cursor() as cursor:
        query = f"""USE {MYSQL_DATABASE};
        CREATE TABLE IF NOT EXISTS orders
        (id INT AUTO_INCREMENT PRIMARY KEY, 
    orderNumber INT,
    orderDate DATE,
    requiredDate DATE,
    shippedDate DATE,
    status VARCHAR(255),
    comments VARCHAR(255),
    customerNumber INT,
    FOREIGN KEY (customerNumber) REFERENCES costumers(customerNumber) )
        """
        cursor.execute(query)
        conn.commit()
        cursor.close()
        

# # create_database()
# # create_table_costumers()
# create_table_orders()