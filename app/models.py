from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique employee ID")
    name: str
    department: str
    salary: float
    joining_date: datetime
    skills: List[str]

class UpdateEmployee(BaseModel):
    name: Optional[str] = Field(None, description="Employee name")
    department: Optional[str] = Field(None, description="Department name")
    salary: Optional[float] = Field(None, description="Employee salary")
    joining_date: Optional[datetime] = Field(None, description="Joining date")
    skills: Optional[List[str]] = Field(None, description="List of skills")

    class Config:
        orm_mode = True
