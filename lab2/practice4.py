from fastapi import FastAPI, Request, Body
import asyncio
# Initialize the FastAPI app
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
    
    ]
@app.get("/members/{crew_id}")
async def read_crew_member(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return {"crew_member": member}
    return {"message": "Crew member not found"}

@app.post("/members/")
async def add_crew_member(data: dict = Body(...)):
    name = data.get("name")
    role = data.get("role")
    crew_id = max([m["id"] for m in crew], default=0) + 1
    new_member = {"id": crew_id, "name": name, "role": role}
    crew.append(new_member)
    return {"crew_member": new_member}

@app.put("/members/{crew_id}")
async def update_crew_member(crew_id: int, request: Request):
    data = await request.json()
    name = data.get("name")
    role = data.get("role")
    for member in crew:
        if member["id"] == crew_id:
            member["name"] = name
            member["role"] = role
            return {"crew_member": member}
    return {"message": "Crew member not found"}

@app.delete("/members/{crew_id}")
async def delete_crew_member(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            crew.remove(member)
            return {"message": f"Crew member {crew_id} deleted", "crew": crew}
    return {"message": "Crew member not found"}

@app.get("/crew/")
async def get_all_crew_members():
    await asyncio.sleep(1)
    return {"crew": crew}


# TODO: Create a GET endpoint to retrieve a specific crew member by ID
# - The endpoint path should be "/members/{crew_id}"
# - The function should be async and named 'read_crew_member'
# - If the crew member is found, return their details in JSON format
# - If not found, return a message indicating the crew member was not found


# TODO: Create a POST endpoint to add a new crew member
# - The endpoint path should be "/members/"
# - The function should be async and named 'add_crew_member'
# - Parse the incoming request to get 'name' and 'role'
# - Create a new crew member with a unique ID and add it to the crew list
# - Return the details of the new crew member


# TODO: Create a PUT endpoint to update an existing crew member's details
# - The endpoint path should be "/members/{crew_id}"
# - The function should be async and named 'update_crew_member'
# - Parse the incoming request to get updated 'name' and 'role'
# - If the crew member is found, update their details
# - If not found, return a message indicating the crew member was not found


# TODO: Create a DELETE endpoint to remove a crew member by ID
# - The endpoint path should be "/members/{crew_id}"
# - The function should be async and named 'delete_crew_member'
# - If the crew member is found, remove them from the crew list
# - If not found, return a message indicating the crew member was not found