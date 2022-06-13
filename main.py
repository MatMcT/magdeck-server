from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from magdeck import MagDeck

deck = MagDeck()
app = FastAPI(title="Magnetic Deck Controller")


# app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/home")
def home():
    return {"success": deck.home()}

@app.get("/api/move/{mm}")
def home(mm):
    return {"success": deck.move(mm)}

@app.get("/api/get-pos")
def get_pos():
    return {"position": deck.get_position()}

@app.get("/api/probe")
def probe():
    return {"position": deck.probe_plate()}

@app.get("/api/get-plate-pos")
def get_plate_pos():
    return {"position": deck.get_plate_position()}