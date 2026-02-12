from mongo_connection import ManagerMongo
import json
from confluent_kafka import Producer, Message
import os 
import asyncio

TOPIC_KAFKA = os.getenv("TOPIC_KAFKA","init_mongo")
PRODUCER_CONFIG = os.getenv('PRODUCER_CONFIG',"localhost:9092")
    

producer = Producer({"bootstrap.servers": PRODUCER_CONFIG})



def publisher(manger :ManagerMongo):
    batch_size = 0
    cursor = 0
    while True:
        batch = manger.collection.find({},skip=batch_size,limit=30).to_list()
        if len(batch) < 30:
            break
        else:
            batch_size += 30
            send_batch(batch)
    if len(batch) > 0:
        send_batch(batch)
    producer.flush()

def send_batch(batch):
    for doc in batch:
        doc['_id'] = str(doc['_id'])
        doc_bytes = serialize_data(doc)
        insert_kafka(doc_bytes)
        asyncio.sleep(0.5)

def serialize_data(data):
    return json.dumps(data).encode("utf-8")

def insert_kafka(data:str):
    producer.produce(
        topic=TOPIC_KAFKA,
        value=data,
        callback=delivery_report
    )

    

producer.flush()