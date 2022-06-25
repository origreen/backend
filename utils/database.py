
from pymongo import MongoClient
from os import getenv

from .score import compute_scores
client = MongoClient(getenv('MONGO_URI'))
db = client.origreen

def get_profiles():
    profiles = db.profiles.find()
    for profile in profiles:
        del profile['_id']
    return profiles

def get_food():
    food = db.food.find()
    for f in food:
        del f['_id']
    return food

def get_food_information(food_id: str):
    food = db.food.find_one({ 'id': food_id })
    del food['_id']
    return food

def get_score(food_id: str): 
    profile = db.profiles.find_one({ 'active': True })
    food_information = get_food_information(food_id)
    return compute_scores(food_information, profile)







