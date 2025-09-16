from fastapi import APIRouter, HTTPException
from .models import Employee, UpdateEmployee
from . import crud
from .utils import serialize_employee  # Convert MongoDB docs into JSON-friendly format

# Initialize API Router
router = APIRouter()

# -------------------------------
# Employee API Endpoints
# -------------------------------

# Create a new employee, Validates unique employee_id before insertion
@router.post("/employees")
async def create_employee(emp: Employee):
    new_emp = await crud.create_employee(emp.model_dump())
    if not new_emp:  # Duplicate employee_id
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    return serialize_employee(new_emp)


# Get employee details by ID
@router.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    emp = await crud.get_employee(employee_id)
    if not emp:  # Employee not found
        raise HTTPException(status_code=404, detail="Employee not found")
    return serialize_employee(emp)


# Update employee details, Only updates fields provided in request (ignores None values)
@router.put("/employees/{employee_id}")
async def update_employee(employee_id: str, emp: UpdateEmployee):
    emp_data = {k: v for k, v in emp.model_dump().items() if v is not None}
    success = await crud.update_employee(employee_id, emp_data)
    if not success:  # No record updated
        raise HTTPException(status_code=404, detail="Employee not found")
    updated_emp = await crud.get_employee(employee_id)  # Fetch updated record
    return serialize_employee(updated_emp)


# Delete employee by ID
@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    success = await crud.delete_employee(employee_id)
    if not success:  # No record deleted
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}


# Get list of employees in a department
# Supports pagination via `skip` and `limit`
@router.get("/employees/department/{department}")
async def list_by_department(
    department: str,
    skip: int = 0,   # Number of records to skip (for pagination)
    limit: int = 10  # Number of records to return
):
    emps = await crud.list_by_department(department, skip=skip, limit=limit)
    return [serialize_employee(emp) for emp in emps]


# Get average salary per department
@router.get("/employees/avg/salary")
async def avg_salary():
    return await crud.avg_salary_by_department()


# Search employees by skills ((e.g., ?skills=Python,SQL))
@router.get("/employees/search/skills")
async def search_employee(skills: str):
    skills_list = [s.strip() for s in skills.split(",")]  # Convert to list
    emps = await crud.search_by_skills(skills_list)
    return [serialize_employee(emp) for emp in emps]
