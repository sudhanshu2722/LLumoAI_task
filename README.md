# Employee Management API

A **FastAPI** application for managing employee data using **MongoDB**.  
Supports CRUD operations, skill-based searches, department-wise listings, and salary analytics.

---

## Features

- Create, Read, Update, and Delete (CRUD) employees
- Search employees by skills
- List employees by department (with pagination)
- Calculate average salary per department
- MongoDB schema validation and unique indexing on `employee_id`
- Asynchronous operations using **Motor** (async MongoDB driver)

---

## Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** MongoDB  
- **Driver:** Motor (async MongoDB)  
- **Python Version:** 3.10+  

---

## Project Structure

.
├── app/
│ ├── crud.py # Database CRUD operations, skill search, analytics
│ ├── database.py # MongoDB connection, schema validation, lifespan
│ ├── main.py # FastAPI app initialization
│ ├── models.py # Pydantic models for validation
│ ├── routes.py # API endpoints
│ ├── utils.py # Serializer for MongoDB documents
├── requirements.txt # Python dependencies
└── README.md


---

## Installation

## 1. Clone the repository:

```bash
git clone <https://github.com/sudhanshu2722/LLumoAI_task/tree/main>
cd <LLUMOAI_TASK>

## 2. Install Dependencies

pip install -r requirements.txt


Ensure MongoDB is running locally at mongodb://localhost:27017.

## Running the API
uvicorn app.main:app --reload

## API Endpoints
Method	  Endpoint	                                       Description
POST	 /employees	                                       Create a new employee
GET	     /employees/{employee_id}                  	       Get employee details by ID
PUT	     /employees/{employee_id}	                       Update employee by ID
DELETE	 /employees/{employee_id}	                       Delete employee by ID
GET	     /employees/department/{department}	               List employees by department (skip and limit query params)
GET	     /employees/avg/salary	                           Get average salary per department
GET	     /employees/search/skills?skills=Python,FastAPI	   Search employees by a comma-separated list of skills


## MONGODB SCHEMA VALIDATION

Ensures all required fields exist
employee_id is unique and indexed
salary must be non-negative
skills is a list of strings
joining_date is stored as a date

## Utils

utils.py contains a serialize_employee function to convert MongoDB documents to JSON-friendly format.

Converts _id to string and joining_date to ISO format.

## Dependencies (requirement.txt)
fastapi==0.111.2
uvicorn[standard]==0.25.0
motor==4.4.0
pydantic==2.6.0


## License
This project is open-source under the MIT License.