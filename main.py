from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import database


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/profiles')
def score():
   
    return dict(database.get_profiles())

@app.get('/food/{id}')
def score(id: str):
    print('DIOCANEEEEEEEEEEEEEEEEEEEEEEE')
    print(database.get_food_information(id))
    print('DIOCANEEEEEEEEEEEEEEEEEEEEEEE')
    return dict(database.get_food_information(id))

@app.get('/food/{id}/score')
def score(id: str):
    return database.get_score(id)
