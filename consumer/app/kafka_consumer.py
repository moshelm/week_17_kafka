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
class ConsumerManager():
    def __init__(self):
        self.consumer = Consumer(CONSUMER_CONFIG)
        self.manager_db : Mysql_Manger = self.init_database()

    def init_database(self):
        try:
            manager = Mysql_Manger()
            manager.create_database()
            manager.create_table_customers()
            manager.create_table_orders()
            return manager
        except Exception as e :
            print(f'create database failed {e}')


    def subscribe(self):
        self.consumer.subscribe([TOPIC_KAFKA])
        print("🟢 Consumer is running and subscribed to orders topic")
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("❌ Error:", msg.error())
                    continue
                
                value = msg.value().decode("utf-8")
                doc : dict = json.loads(value)
        
                table_name = doc['type']+'s'
                del doc['type']
                columns = []
                values = []
                for key, value in doc.items():
                    if key == 'type'or '_id'==key:
                        continue
                    if value:
                        columns.append(key)
                        values.append(value)
                self.manager_db.insert_one(table_name,columns,values)
                try:
                    print(f"📦 Received doc.")
                except Exception as e:
                    print(doc,e)
        except KeyboardInterrupt:
            print("\n🔴 Stopping consumer")

        finally:
            self.consumer.close()