
from pymongo import MongoClient
from os import getenv

from .score import compute_scores
client = MongoClient(getenv('MONGO_URI'))
db = client.origreen

def get_profiles():
    profiles = list(db.profiles.find())
    for profile in profiles:
        del profile['_id']
    return profiles

def get_food():
    food = list(db.food.find())
    for f in food:
        del f['_id']
    return food

def get_active_profile():
    profile = db.profiles.find_one({ 'active': True })
    del profile['_id']
    return profile

def set_active_profile(name: str):
    db.profiles.update_many({ 'active': True }, { '$set': { 'active': False } })
    db.profiles.update_one({ 'name': name }, { '$set': { 'active': True } })

def set_update_custom_profile(name: str, value: float):
    profile = db.profiles.find_one({ 'name': 'custom' })

    if name == 'nutritional':
        profile['parameters']['nutritional']['weight'] = value
    elif name == 'vitamins':
        profile['parameters']['nutritional']['parameters']['vitamins']['weight'] = value
    elif name == 'fibers':
        profile['parameters']['nutritional']['parameters']['fibers']['weight'] = value
    elif name == 'calories':
        profile['parameters']['nutritional']['parameters']['calories']['weight'] = value
    elif name == 'sodium':
        profile['parameters']['nutritional']['parameters']['sodium']['weight'] = value
    elif name == 'environmental':
        profile['parameters']['environmental']['weight'] = value
    elif name == 'water':
        profile['parameters']['environmental']['parameters']['water']['weight'] = value
    elif name == 'energy':
        profile['parameters']['environmental']['parameters']['energy']['weight'] = value
    elif name == 'co2':
        profile['parameters']['environmental']['parameters']['co2']['weight'] = value

    db.profiles.update_one({ 'name': 'custom' }, { '$set': profile })


def get_food_information(food_id: str):
    food = db.food.find_one({ 'id': food_id })
    del food['_id']
    return food

def get_score(food_id: str): 
    profile = get_active_profile()
    food_information = get_food_information(food_id)
    return compute_scores(food_information, profile)







