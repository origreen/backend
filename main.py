from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils import database

class SetActiveBody(BaseModel):
    name: str
class UpdateCustomProfileBody(BaseModel):
    name: str
    value: float


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/profiles')
def profiles():
    return database.get_profiles()

@app.get('/profiles/active')
def profiles():
    return database.get_active_profile()

@app.post('/profiles/active')
def profiles(body: SetActiveBody):
    return database.set_active_profile(body.name)

@app.post('/profiles/custom')
def profiles(body: UpdateCustomProfileBody):
    return database.set_update_custom_profile(body.name, body.value)

@app.get('/food')
def food():
    return database.get_food()

@app.get('/food/{id}')
def foodId(id: str):
    return dict(database.get_food_information(id))

@app.get('/food/{id}/score')
def foodScore(id: str):
    return database.get_score(id)
