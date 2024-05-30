from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os


# async def connect_db():
#     load_dotenv()
#     try:
#         uri = os.getenv("MONGODB_URL_LOCAL")
#         client = MongoClient(uri, tls=True)
#         return client
#     except Exception as e:
#         return e



uri = os.getenv("MONGODB_URL_LOCAL")

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
