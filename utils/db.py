import os

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

cluster = MongoClient(os.getenv('MONGO_URI'))
db = cluster['jaxie']

async def create_server_collection(guild_id):
    db['roles'].insert_one({
        "_id": guild_id,
        "autoroles": [],
        "reactroles": {}
    })

async def clear_server_data(guild_id):
    try:
        db['roles'].delete_one(db['roles'].find_one({'_id': guild_id}))
        db['welcome'].delete_one(db['welcome'].find_one({'_id': guild_id}))
    except Exception as e:
        return [False, e]
    return True
