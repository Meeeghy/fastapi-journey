from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CategoryType(str, Enum):
    food = "food"
    transport = "transport"
    shopping = "shopping"
    bills = "bills"


class Category(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    type: CategoryType


class Transaction(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=50)
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    categories: List[Category] = []

