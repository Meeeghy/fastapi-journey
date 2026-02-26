from fastapi import FastAPI

app = FastAPI()

crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob",   "role": "Scientist"},
]

@app.get("/crew_with_path/{crew_id}")
def get_crew_by_path(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member
    return {"message": "Crew member not found"}

@app.get("/crew_with_query/member")
def get_crew_by_query(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member
    return {"message": "Crew member not found"}
