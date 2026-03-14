from fastapi import FastAPI, Request
from models import Transaction
import asyncio

app = FastAPI()

fake_db = []

@app.get("/transactions/")
async def read_transaction():
    return fake_db

@app.get("/transactions/{transaction_id}")
async def read_transaction_byId(transaction_id: int):
    await asyncio.sleep(1)
    for t in fake_db:
        if t.id == transaction_id:
            return t
    return {"message": "Transaction not found"}

@app.post("/transactions/")
async def add_transaction(transaction: Transaction):
    await asyncio.sleep(1) 
    transaction_id = max(a["id"] for a in fake_db) + 1 if fake_db else 1 
    fake_db.append(transaction)
    return {"message": "Transaction added successfully", "details": transaction}

@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, request: Request):
    data = await request.json()
    for t in fake_db:
        if t.id == transaction_id:
            t.title = data.get("title", t.title)
            t.amount = data.get("amount", t.amount)
            t.description = data.get("description", t.description)
            t.categories = data.get("categories", t.categories)
            return {"message": "Transaction updated", "details": t}
    return {"message": "Transaction not found"}

@app.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int):
    for t in fake_db:
        if t.id == transaction_id:
            fake_db.remove(t)
            return {"message": f"Transaction {transaction_id} deleted"}
    return {"message": "Transaction not found"}
    
        
     
     



 