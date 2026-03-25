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

## Database

1. `@contextmanager` is a decorator that lets us use a function with the `with` statement. We use it because it automatically closes the database connection when we are done — even if something goes wrong. Without it, we would have to remember to call `db.close()` manually every time, which is easy to forget.

2. `check_same_thread=False` allows SQLite to work with FastAPI. FastAPI handles multiple requests at the same time using different threads, and by default SQLite only allows one thread to use it. Setting this to `False` removes that restriction so our app works correctly.

3. With the old list (`fake_db = []`), all data disappears every time the server restarts because it only exists in memory — like RAM. With SQLite, data is saved to a real file (`sqlite.db`) on the computer, so it stays there even after the server restarts.