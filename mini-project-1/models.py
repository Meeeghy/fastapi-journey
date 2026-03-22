from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Category_Type(str, Enum):
    income = "income"
    expense = "expense"

class Category(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    type: Category_Type

class Transaction(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0)
    description: Optional[str] = None
    categories: List[Category] = Field(default=[]) 

