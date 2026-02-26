from fastapi import FastAPI

ahmed = FastAPI()

@ahmed.get("/")
def read_root():
    return {"message": "Hello, Practice 1!"}
