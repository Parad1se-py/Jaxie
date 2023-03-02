from .db import *


collection = db['roles']


def add_autorole(guild_id, role_id) -> bool:
    # check if collection already exists in database,
    # if not then create a collection
    if not bool(collection.find_one({"_id": guild_id})):
        collection.insert_one({
            "_id": guild_id,
            "autoroles": [role_id],
            "reactroles": {}
        })
        return True

    # update if collection exists
    collection.update_one({"_id": guild_id}, {"$push": {"autoroles": role_id}})
    return True

def remove_autorole(guild_id, role_id) -> bool:
    # checks if collection exists in database. if it does,
    # it deletes the role from it, else returns False
    coll = collection.find_one({"_id": guild_id})
    
    if not bool(coll):
        return False

    # delete role from db
    collection.update_one(
        {"_id": guild_id},
        {"$pull": {"autoroles": role_id}}
    )
    return True

def fetch_autoroles(guild_id) -> list:
    # fetch the collection
    guild = collection.find_one({"_id": guild_id})
    # return false if collection doesn't exist else the roles.
    return guild["autoroles"] if bool(guild) else [False]

def add_reactrole(guild_id, message_id, *args):
    reactroles = {{key: val} for key, val in args[0]}

    if not bool(collection.find_one({"_id": guild_id})):
        collection.insert_one({
            "_id": guild_id,
            "autoroles": [],
            "reactroles": {message_id: reactroles}
        })
        return True

    collection.update_one(
        {"_id": guild_id},
        {"$update": {"reactroles": {message_id: reactroles}}}
    )
    return True

def fetch_reactrole(guild_id, message_id):
    coll = collection.find_one({"_id": guild_id})
    return coll['reactroles'][message_id] if bool(coll) else False
