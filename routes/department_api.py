from pymongo.errors import DuplicateKeyError
from sanic import Blueprint, response
from sanic_ext.extensions.openapi import openapi
from sanic.exceptions import NotFound
from config.db import db_connection
from models.department_model import department_entity, departments_entity
from schema.department_schema import Department

from bson import ObjectId

department_api = Blueprint('department', url_prefix='Department')


@department_api.get('/')
async def get_all_departments(request):
    departments_cursor = db_connection.department.find()
    departments = departments_entity(departments_cursor)
    if not departments:
        raise NotFound("Database is empty")
    return response.json(departments)


@department_api.post('/')
@openapi.definition(body={'application/json': Department.model_json_schema()}, tag='department')
async def create_department(request):
    department_data = request.json
    try:
        user_id = db_connection.department.insert_one(dict(department_data)).inserted_id
        user = db_connection.department.find_one({"_id": user_id})
        return response.json({"message": 'User Added Successfully', 'user': department_entity(user)}, status=201)
    except DuplicateKeyError:
        return response.json({"error": "User already exists"}, status=409)


@department_api.delete('/delete_doctor/<department_id:str>')
async def delete_department(request, department_id):
    try:
        department_object_id = ObjectId(department_id)

        # Find the existing doctor document
        existing_department = db_connection.department.find_one({"_id": department_object_id})
        if existing_department:
            db_connection.doctor.delete_one({"_id": department_object_id})

            response_data = {
                "deleted_doctor_id": str(existing_department),
                "message": "Doctor deleted successfully"
            }
            return response.json(response_data)
        else:
            return response.json({"message": "Doctor not found"}, status=404)

    except ValueError:
        return response.json({"message": "Incorrect _id"}, status=404)
    except TypeError:
        return response.json({"message": "Unable to process request"}, status=500)


@department_api.put('/update/<department_id:str>')
@openapi.definition(body={'application/json': Department.model_json_schema()}, tag='department')
async def update_doctor(request, department_id):
    try:
        department_data = request.json
        department_object_id = ObjectId(department_id)
        db_connection.department.find_one_and_update({"_id": department_object_id}, {
            "$set": dict(department_data)
        })
        # updated_doctor = departments_entity(db_connection.doctor.find_one({"_ id": department_object_id}))
        return response.json({"message": "Doctor Updated Successfully"}, status=200)

    except ValueError:
        return response.json({"message": "Incorrect Id"})
