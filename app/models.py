from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ---------------------------------------
# Employee Schema Definitions (Pydantic)
# ---------------------------------------

# Schema for creating a new employee
class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique employee ID")  # Required field
    name: str                                                        # Employee name
    department: str                                                  # Department name
    salary: float                                                    # Employee salary
    joining_date: datetime                                           # Date of joining (ISO format)
    skills: List[str]                                                # List of skills


# Schema for updating employee details
# All fields are optional, so only specified ones get updated
class UpdateEmployee(BaseModel):
    name: Optional[str] = Field(None, description="Employee name")
    department: Optional[str] = Field(None, description="Department name")
    salary: Optional[float] = Field(None, description="Employee salary")
    joining_date: Optional[datetime] = Field(None, description="Joining date")
    skills: Optional[List[str]] = Field(None, description="List of skills")

    class Config:
        orm_mode = True  # Allows compatibility with ORMs (if used in future)
