from mongo_connection import ManagerMongo
from kafka_publisher import publisher

manger = ManagerMongo()
manger.init_collection()
publisher(manger)