from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain", "experience": 10, "specialty": "Leadership"},
    {"id": 2, "name": "Alice", "role": "Engineer", "experience": 8, "specialty": "Mechanical"},
    {"id": 3, "name": "Bob", "role": "Scientist", "experience": 5, "specialty": "Biology"}
]


# TODO: Define a Pydantic model for the crew member with:
# - name
# - role
# - experience
# - specialty
class CrewMember(BaseModel):
    name: str
    role: str
    experience: int
    specialty: str

# TODO: Define a POST endpoint receiving a crew member model
# Use the code provided in the description to handle the database and response

@app.get("/crew/{crew_id}", response_model=CrewMember)
async def read_crew_member(crew_id : int):
    for member in crew:
        if member["id"] == crew_id:
         return member
    return {"message":"this member not found"}


@app.post("/crew/")
async def add_new_member(member: CrewMember):
    crew_id = max(a["id"] for a in crew) + 1 if crew else 1 
    new_member ={
        "id" : crew_id,
        "name": member.name,
        "role": member.role,
        "experience": member.experience,
        "specialty" : member.specialty
    }
    
    crew.append(new_member)
    return {"message": "member info added successfully", "details": new_member}