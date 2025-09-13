from datetime import datetime, date
from bson import ObjectId

def serialize_employee(emp: dict):
    """Convert MongoDB document to JSON-friendly dictionary"""
    if not emp:
        return None

    # Convert ObjectId to string
    if "_id" in emp and isinstance(emp["_id"], ObjectId):
        emp["_id"] = str(emp["_id"])

    # Convert datetime to string
    if "joining_date" in emp and isinstance(emp["joining_date"], (datetime, date)):
        emp["joining_date"] = emp["joining_date"].isoformat()

    return emp
