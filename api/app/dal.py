from connection import Mysql_Manger

db = Mysql_Manger()

def top_customers():
    query = """SELECT c.customerNumber, 
    c.customerName, 
    COUNT(o.id) AS total_orders FROM customers c join orders o on c.customerNumber=o.customerNumber
    GROUP BY c.customerNumber, c.customerName
    ORDER BY total_orders DESC
    LIMIT %s;"""
    params = (10,)
    return db.query(query,params)


# Route 2
def get_inactive_customers():
    sql = """
    SELECT c.customerNumber, c.customerName 
    FROM customers c 
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber 
    WHERE o.customerNumber IS NULL
    """
    return db.query(sql)

# Route 3
def get_zero_credit_active_customers():
    sql = """
    SELECT c.customerNumber, c.customerName, COUNT(o.id) as order_count 
    FROM customers c 
    JOIN orders o ON c.customerNumber = o.customerNumber 
    WHERE c.creditLimit = 0 
    GROUP BY c.customerNumber
    """
    return db.query(sql)