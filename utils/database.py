
from pymongo import MongoClient
from os import getenv

from .score import compute_scores
print(getenv('MONGO_URI'))
client = MongoClient(getenv('MONGO_URI'))
db = client.origreen

def get_score(food_id: str) -> str: 
    profile = db.profiles.find_one({ 'active': True })
    food_information = db.food.find_one({ 'id': food_id })
    return compute_scores(food_information, profile)







