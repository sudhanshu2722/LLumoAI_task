from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from pymongo.errors import CollectionInvalid

# ===============================
# MongoDB Client & Database Setup
# ===============================

# Create MongoDB client (asynchronous)
client = AsyncIOMotorClient("mongodb://localhost:27017")

# Use (or create) the database named "assessment_db"
db = client["assessment_db"]

# Reference to the "employees" collection
employees_collection = db.get_collection("employees")


# =============================
# JSON Schema for Validation
# =============================
# Ensures that inserted employee documents
# follow the correct structure and data types.
schema = {
    "bsonType": "object",
    "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
    "properties": {
        "employee_id": {"bsonType": "string"},               # Must be a string
        "name": {"bsonType": "string"},                      # Must be a string
        "department": {"bsonType": "string"},                # Must be a string
        "salary": {"bsonType": "double", "minimum": 0},      # Must be non-negative float
        "joining_date": {"bsonType": "date"},                # Must be a valid date
        "skills": {"bsonType": "array", "items": {"bsonType": "string"}},  # List of strings
    },
}


# ===============================
# FastAPI Lifespan Event Handler
# ===============================
# Runs setup tasks on app startup, and cleanup on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Create "employees" collection with schema validation
        await db.create_collection("employees", validator={"$jsonSchema": schema})
        print("Collection created with schema validation")
    except CollectionInvalid:
        # Collection already exists → just log
        print("Collection already exists")

    # Ensure unique index on "employee_id" to prevent duplicates
    await employees_collection.create_index(
        "employee_id",
        unique=True,
        name="unique_employee_id_index"
    )
    print("Index ensured on employee_id")

    yield  # Hand control back to FastAPI

    # Shutdown
    # Close MongoDB connection when app stops
    client.close()
    print("🔴 MongoDB connection closed")


# ============================
# FastAPI App Initialization
# ============================
# Passing lifespan event handler to manage startup/shutdown
app = FastAPI(lifespan=lifespan)
