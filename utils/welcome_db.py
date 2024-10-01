from .db import *


collection = db['welcome']

def check_welcome(guild_id:int) -> bool:
    ...

def set_welcome(guild_id:int, channel_id:int):
    ...

def unset_welcome(guild_id:int, channel_id:int):
    ...

def update_welcome(guild_id:int, channel_id:int):
    ...
