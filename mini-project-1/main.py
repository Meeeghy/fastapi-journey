from fastapi import FastAPI
from typing import List
import asyncio

from models import Transaction

app = FastAPI()

transactions: List[Transaction] = []

@app.get("/transactions/")
async def get_transactions():
    return transactions

@app.get("/transactions/{id}")
async def get_transaction(id: int):
    for transaction in transactions:
        if transaction.id == id:
            return transaction
    return {"message": "Transaction not found"}

@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    await asyncio.sleep(1)  
    transactions.append(transaction)
    return transaction

@app.put("/transactions/{id}")
async def update_transaction(id: int, updated: Transaction):
    for i, transaction in enumerate(transactions):
        if transaction.id == id:
            transactions[i] = updated
            return updated
    return {"message": "Transaction not found"}


@app.delete("/transactions/{id}")
async def delete_transaction(id: int):
    for i, transaction in enumerate(transactions):
        if transaction.id == id:
            deleted = transactions.pop(i)
            return deleted
    return {"message": "Transaction not found"}

