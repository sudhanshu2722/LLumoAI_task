from fastapi import APIRouter,HTTPException
from .models import Employee, UpdateEmployee
from . import crud
from .utils import serialize_employee  # import serializer
router = APIRouter()


@router.post("/employees")
async def create_employee(emp: Employee):
    new_emp = await crud.create_employee(emp.model_dump())
    if not new_emp:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    return serialize_employee(new_emp)

@router.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    emp = await crud.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return serialize_employee(emp)

@router.put("/employees/{employee_id}")
async def update_employee(employee_id: str, emp: UpdateEmployee):
    print(employee_id, emp)
    emp_data = {k: v for k, v in emp.model_dump().items() if v is not None}
    success = await crud.update_employee(employee_id, emp_data)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated_emp = await crud.get_employee(employee_id)
    return serialize_employee(updated_emp)

@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    success = await crud.delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@router.get("/employees/department/{department}")
async def list_by_department(
    department: str,
    skip: int = 0,   # number of records to skip
    limit: int = 10  # number of records to return
):
    emps = await crud.list_by_department(department, skip=skip, limit=limit)
    return [serialize_employee(emp) for emp in emps]


@router.get("/employees/avg/salary")
async def avg_salary():
    return await crud.avg_salary_by_department()

@router.get("/employees/search/skills")
async def search_employee(skills: str):
    # split comma-separated string into list
    skills_list = [s.strip() for s in skills.split(",")]
    print("Searching for skills:", skills_list)
    emps = await crud.search_by_skills(skills_list)
    return [serialize_employee(emp) for emp in emps]

