from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware          # CORS
from pydantic import BaseModel                              # Interfacce
from datetime import datetime
import json, os, csv, hashlib
from starlette.responses import FileResponse

# Swagger
description = """
AirQualityAPI - Manuel Tonello 🍅
"""

app = FastAPI(
    title="AQA Swagger",
    description=description,
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "Manuel Tonello",
        "email": "tomatosaucestaff@gmail.com",
    },
    #license_info = {"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html",},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReturnHomepage(BaseModel):
    message: str

@app.get("/", response_model = ReturnHomepage)
async def test_api():
    return ReturnHomepage(message = "/docs for the documentation.")



class SaveDataModel(BaseModel):
    password: str
    city: str
    humidity: float
    temperature: float
    quality: float

class ReturnSaveDataModel(BaseModel):
    success: bool
    error: Optional[str] = None

@app.post("/saveData", response_model=ReturnSaveDataModel)
def save_data(data: SaveDataModel):
    enc_pw = hashlib.sha256(data.password.encode()).hexdigest()
    if enc_pw != ":)":
        return ReturnSaveDataModel(success = False, error = "Wrong password!")

    try:
        now = "{}".format(datetime.now())
        row = [now, data.city, data.humidity, data.temperature, data.quality]
        if not os.path.exists('AQAtomato.csv'):                                     # if file doesn't exists
            header = ['date', 'city', 'humidity', 'temperature', 'quality']

            with open('AQAtomato.csv', 'w+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)                                             # add headers
                writer.writerow(row)
        else:
            with open('AQAtomato.csv', 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)                                                # else, don't
        return ReturnSaveDataModel(success = True)
    except:
        return ReturnSaveDataModel(success = False, error = "Error adding the new row.")



@app.get("/getData", response_model = ReturnHomepage)
async def get_saved_data():
    if not os.path.exists('AQAtomato.csv'):
        return ReturnHomepage(message = "File not found.")
    return FileResponse('AQAtomato.csv', media_type='application/octet-stream', filename='AQAtomato.csv')