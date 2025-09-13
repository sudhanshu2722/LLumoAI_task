from .database import employees_collection

async def create_employee(emp: dict):
    existing = await employees_collection.find_one({"employee_id": emp["employee_id"]})
    if existing:
        return None
    await employees_collection.insert_one(emp)
    return emp

async def get_employee(emp_id: str):
    return await employees_collection.find_one({"employee_id": emp_id})

async def update_employee(emp_id: str, data: dict):
    print(emp_id, data)
    result = await employees_collection.update_one(
        {"employee_id": emp_id}, {"$set": data}
    )
    print(result)
    return result.modified_count > 0

async def delete_employee(emp_id: str):
    result = await employees_collection.delete_one({"employee_id": emp_id})
    return result.deleted_count > 0

async def list_by_department(department: str, skip: int = 0, limit: int = 10):
    cursor = (
        employees_collection.find({"department": department})
        .sort("joining_date", -1)
        .skip(skip)
        .limit(limit)
    )
    return await cursor.to_list(length=limit)


async def avg_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}}
    ]
    return await employees_collection.aggregate(pipeline).to_list(length=100)

async def search_by_skills(skills: list[str]):
    cursor = employees_collection.find({"skills": {"$all": skills}})
    return await cursor.to_list(length=100)

