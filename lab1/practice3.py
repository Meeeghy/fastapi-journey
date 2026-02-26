from fastapi import FastAPI   # TODO: Import FastAPI

app = FastAPI()               # TODO: Initialize FastAPI app

@app.get("/")                 # TODO: Define root endpoint
def read_root():
    return {"message": "Greetings from your FastAPI spaceship!"}