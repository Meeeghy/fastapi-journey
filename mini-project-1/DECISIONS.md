# DECISIONS.md

## 1. Why I chose each Pydantic field type

- `id: int` — IDs are whole numbers, no decimals needed
- `title: str` — the transaction name is text
- `amount: float` — money can have decimals like 9.99
- `description: Optional[str]` — not every transaction needs a description, so it can be empty
- `categories: List[Category]` — a transaction can have more than one category
- `name: str` — category name is text
- `type: Category_Type` — category type can only be "income" or "expense", nothing else

## 2. What each validation rule protects against

- `id: Field(ge=1)` — prevents using 0 or negative numbers as an ID
- `title: Field(min_length=2, max_length=50)` — prevents empty or too long titles
- `amount: Field(gt=0)` — prevents adding a transaction with zero or negative money
- `description: Optional` — allows the user to skip the description without getting an error
- `Category_Type (enum)` — prevents invalid types like "random" or "salary"
- `name: Field(min_length=2, max_length=20)` — prevents empty or too long category names

## 3. Which endpoint uses async in a meaningful way and why

All endpoints use `async def` because FastAPI works well with asynchronous functions.

The `GET /transactions/{transaction_id}` endpoint uses `await asyncio.sleep(1)` 
to simulate a delay, like when fetching data from a real database.
This shows how async can handle waiting without freezing the whole server.