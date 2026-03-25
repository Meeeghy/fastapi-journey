from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Transaction
from database import managed_db

transaction_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@transaction_router.get("/transactions/")
async def read_transaction():
    with managed_db() as db:
        return db.get_all()

@transaction_router.get("/transactions/{transaction_id}")
async def read_transaction_byId(transaction_id: int):
    with managed_db() as db:
        transaction = db.get(transaction_id)
        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with ID {transaction_id} was not found"
            )
        return transaction

@transaction_router.post("/transactions/")
async def add_transaction(transaction: Transaction):
    with managed_db() as db:
        new_id = db.create(transaction)
        return {"message": "Transaction added successfully", "id": new_id}

@transaction_router.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: Transaction):
    with managed_db() as db:
        updated = db.update(transaction_id, transaction)
        if updated is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with ID {transaction_id} was not found"
            )
        return {"message": "Transaction updated", "details": updated}

@transaction_router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int):
    with managed_db() as db:
        transaction = db.get(transaction_id)
        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with ID {transaction_id} was not found"
            )
        db.delete(transaction_id)
        return {"message": f"Transaction {transaction_id} deleted"}

@transaction_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    with managed_db() as db:
        transactions = db.get_all()
    return templates.TemplateResponse("transaction.html", {
        "request": request,
        "transactions": transactions
    })

@transaction_router.get("/transaction/{id}", response_class=HTMLResponse)
async def get_transaction_page(request: Request, id: int):
    with managed_db() as db:
        transaction = db.get(id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return templates.TemplateResponse("transaction.html", {
        "request": request,
        "transaction": transaction
    })