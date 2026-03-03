from fastapi import FastAPI, Request 
import asyncio

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]

@app.get("/crew/")
async def get_all_crew_members():
    await asyncio.sleep(3)
    return {"crew":crew}


@app.post("/add_crew/")
async def add_crew_member(request: Request):
    data = await request.json()

    name = data["name"]
    role = data["role"]

    crew_id = max(member["id"] for member in crew) + 1 if crew else 1

    new_member = {
        "id": crew_id,
        "name": name,
        "role": role
    }

    
    crew.append(new_member)

    
    return {"crew": crew_id, "crew_member": new_member}