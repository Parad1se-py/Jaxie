import os

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

cluster = MongoClient(os.getenv('MONGO_URI'))
db = cluster['jaxie']
