from fastapi import FastAPI
# Just imports FastAPI, nothing else needed here

from transaction import transaction_router
# Goes into transaction.py and grabs the router
# This is how main.py "knows about" all your endpoints

app = FastAPI()
# Creates the app — same as before

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to the Budget Tracker API"}
# The ONLY endpoint that stays in main.py
# Just a welcome message at the root "/"

app.include_router(transaction_router)
# This CONNECTS all your transaction endpoints into the app
# Without this line, none of your /transactions/ routes would work
# It's like plugging in the kitchen to the restaurant