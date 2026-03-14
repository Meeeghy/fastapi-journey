# DECISIONS.md

## 1. Why I chose each Pydantic field type

I used Pydantic models to organize the data in my API.

For the **Transaction** model, I used `int` for `id` because each transaction needs a unique number.
I used `str` for `title` because it stores the name or short description of the transaction.
The `amount` is a `float` because money values can include decimals.
The `description` is `Optional[str]` because sometimes a transaction may not need extra details.
The `categories` field is a `List[Category]` since one transaction can have one or more categories.

For the **Category** model, the `name` is a `str` because it stores the category name.
The `type` is an `Enum` so that only specific category types are allowed.

---

## 2. What each validation rule protects against

The validation rules help make sure the data sent to the API is correct.

The `min_length` and `max_length` for strings make sure the text is not too short or too long.
The `amount` field uses `gt=0` to make sure the transaction amount is positive.
The `Enum` for category type makes sure only allowed values are used.
The optional `description` allows the user to leave it empty if they want.

---

## 3. Which endpoint uses async in a meaningful way and why

All endpoints use `async def` because FastAPI works well with asynchronous functions.

The `POST /transactions/` endpoint uses `await asyncio.sleep(1)` to simulate a delay, like when saving data to a database.
This shows how async can handle waiting operations while the server continues working.
