from .database import employees_collection
from typing import Optional, List, Dict


# -------------------------------
# CRUD Operations on Employee Data
# -------------------------------

# Create a new employee document in MongoDB
# Ensures that employee_id is unique before inserting
async def create_employee(emp: dict) -> Optional[dict]:
    existing = await employees_collection.find_one({"employee_id": emp["employee_id"]})
    if existing:   # Prevent duplicate employee IDs
        return None
    await employees_collection.insert_one(emp)
    return emp


# Retrieve a single employee record by employee_id
async def get_employee(emp_id: str) -> Optional[dict]:
    return await employees_collection.find_one({"employee_id": emp_id})


# Update an employee record by employee_id
# Returns True if any record was modified, else False
async def update_employee(emp_id: str, data: dict) -> bool:
    result = await employees_collection.update_one(
        {"employee_id": emp_id}, {"$set": data}  # Apply only provided updates
    )
    return result.modified_count > 0


# Delete an employee record by employee_id
# Returns True if a record was deleted, else False
async def delete_employee(emp_id: str) -> bool:
    result = await employees_collection.delete_one({"employee_id": emp_id})
    return result.deleted_count > 0


# List employees in a given department
# Supports pagination with skip & limit
# Sorts by joining_date (newest first)
async def list_by_department(
    department: str, skip: int = 0, limit: int = 10
) -> List[dict]:
    cursor = (
        employees_collection.find({"department": department})
        .sort("joining_date", -1)   # Sort in descending order
        .skip(skip)                 # Skip N records (for pagination)
        .limit(limit)               # Limit results
    )
    return await cursor.to_list(length=limit)


# Compute the average salary grouped by department
async def avg_salary_by_department() -> List[Dict[str, float]]:
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}}  # Restructure output
    ]
    return await employees_collection.aggregate(pipeline).to_list(length=100)


# Search employees by required skill set
# Matches employees having ALL the given skills
async def search_by_skills(skills: List[str]) -> List[dict]:
    cursor = employees_collection.find({"skills": {"$all": skills}})
    return await cursor.to_list(length=100)
