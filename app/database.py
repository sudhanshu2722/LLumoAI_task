from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from pymongo.errors import CollectionInvalid

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["assessment_db"]
employees_collection = db.get_collection("employees")

# JSON Schema for validation
schema = {
    "bsonType": "object",
    "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
    "properties": {
        "employee_id": {"bsonType": "string"},
        "name": {"bsonType": "string"},
        "department": {"bsonType": "string"},
        "salary": {"bsonType": "double", "minimum": 0},
        "joining_date": {"bsonType": "date"},
        "skills": {"bsonType": "array", "items": {"bsonType": "string"}},
    },
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup ----
    try:
        await db.create_collection("employees", validator={"$jsonSchema": schema})
        print("✅ Collection created with schema validation")
    except CollectionInvalid:
        print("⚠️ Collection already exists")

    await employees_collection.create_index(
        "employee_id",
        unique=True,
        name="unique_employee_id_index"
    )
    print("✅ Index ensured on employee_id")

    yield  # Hand control back to FastAPI

    # ---- Shutdown ----
    client.close()
    print("🔴 MongoDB connection closed")

app = FastAPI(lifespan=lifespan)
