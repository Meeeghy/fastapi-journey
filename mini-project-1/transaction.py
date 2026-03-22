from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Transaction

transaction_router = APIRouter()

templates = Jinja2Templates(directory="templates")

fake_db = []

@transaction_router.get("/transactions/")
async def read_transaction():
    return fake_db

@transaction_router.get("/transactions/{transaction_id}")
async def read_transaction_byId(transaction_id: int):
    for t in fake_db:
        if t.id == transaction_id:
            return t
    raise HTTPException(
        status_code=404,
        detail=f"Transaction with ID {transaction_id} was not found"
    )

@transaction_router.post("/transactions/")
async def add_transaction(transaction: Transaction):
    # automatically generate the next id
    transaction.id = max((t.id for t in fake_db), default=0) + 1
    fake_db.append(transaction)
    return {"message": "Transaction added successfully", "details": transaction}

@transaction_router.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, request: Request):
    data = await request.json()
    for t in fake_db:
        if t.id == transaction_id:
            t.title = data.get("title", t.title)
            t.amount = data.get("amount", t.amount)
            t.description = data.get("description", t.description)
            t.categories = data.get("categories", t.categories)
            return {"message": "Transaction updated", "details": t}
    raise HTTPException(
        status_code=404,
        detail=f"Transaction with ID {transaction_id} was not found"
    )

@transaction_router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int):
    for t in fake_db:
        if t.id == transaction_id:
            fake_db.remove(t)
            return {"message": f"Transaction {transaction_id} deleted"}
    # raise proper 404 error instead of returning plain dict
    raise HTTPException(
        status_code=404,
        detail=f"Transaction with ID {transaction_id} was not found"
    )

@transaction_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("transaction.html", {
        "request": request,
        "transactions": fake_db
    })

@transaction_router.get("/transaction/{id}", response_class=HTMLResponse)
async def get_transaction_page(request: Request, id: int):
    for t in fake_db:
        if t.id == id:
            return templates.TemplateResponse("transaction.html", {
                "request": request,
                "transaction": t
            })
    raise HTTPException(status_code=404, detail="Transaction not found")