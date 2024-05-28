from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

uri = os.getenv("MONGODB_URL")

app = FastAPI()


client = MongoClient(uri, tls=True)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.get("/")
def home():
    return {"Hello": "World!"}
