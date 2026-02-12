import json
import os 
from confluent_kafka import Consumer
from mysql_connection import Mysql_Manger

TOPIC_KAFKA = os.getenv("TOPIC_KAFKA","init_mongo")
PRODUCER_CONFIG = os.getenv('PRODUCER_CONFIG',"localhost:9092")
    
CONSUMER_CONFIG = {
    "bootstrap.servers": PRODUCER_CONFIG,
    "group.id": "order-tracker",
    "auto.offset.reset": "earliest"
}
mysql = Mysql_Manger()
mysql.create_database()
mysql.create_table_costumers()
mysql.create_table_orders()

consumer = Consumer(CONSUMER_CONFIG)

consumer.subscribe([TOPIC_KAFKA])

print("🟢 Consumer is running and subscribed to orders topic")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Error:", msg.error())
            continue
        
        value = msg.value().decode("utf-8")
        doc :dict= json.loads(value)
        if doc['type'] == 'costumer':
            table_name = doc['type']
            del doc['type']
            columns = []
            values = []
            for key, value in doc.items():
                if value:
                    columns.append(key)
                    values.append(value)
            mysql.insert_one(table_name,columns,values)


        print(f"📦 Received order: {order['quantity']} x {order['item']} from {order['user']}")
except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    consumer.close()