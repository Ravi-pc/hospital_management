from pymongo.errors import DuplicateKeyError
from sanic import Blueprint, response
from sanic_ext.extensions.openapi import openapi
from sanic.exceptions import NotFound
from config.db import db_connection
from models.doctor_model import doctor_entity, doctors_entity
from schema.doctor_schema import Doctor
from bson import ObjectId

doctor_api = Blueprint('doctor', url_prefix='Doctor')


@doctor_api.get('/')
async def get_all_doctors(request):
    doctors = doctors_entity(db_connection.doctor.find())
    if not doctors:
        raise NotFound("Database is empty")
    return response.json(doctors)


@doctor_api.post('/')
@openapi.definition(body={'application/json': Doctor.model_json_schema()}, tag='doctor')
async def create_doctor(request):
    doctor_data = request.json
    try:
        user_id = db_connection.doctor.insert_one(dict(doctor_data)).inserted_id
        user = db_connection.doctor.find_one({"_id": user_id})
        return response.json({"message": 'User Added Successfully', 'user': doctor_entity(user)}, status=201)
    except DuplicateKeyError:
        return response.json({"error": "User already exists"}, status=409)


@doctor_api.delete('/delete_doctor/<doctor_id:str>')
async def delete_doctor(request, doctor_id):
    try:
        doctor_object_id = ObjectId(doctor_id)

        # Find the existing doctor document
        existing_doctor = db_connection.doctor.find_one({"_id": doctor_object_id})
        if existing_doctor:
            db_connection.doctor.delete_one({"_id": doctor_object_id})

            response_data = {
                "deleted_doctor_id": str(existing_doctor),
                "message": "Doctor deleted successfully"
            }
            return response.json(response_data)
        else:
            return response.json({"message": "Doctor not found"}, status=404)

    except ValueError:
        return response.json({"message": "Incorrect _id"}, status=404)
    except TypeError:
        return response.json({"message": "Unable to process request"}, status=500)


@doctor_api.put('/update/<doctor_id:str>')
@openapi.definition(body={'application/json': Doctor.model_json_schema()}, tag='doctor')
async def update_doctor(request, doctor_id):
    try:
        doctor_data = request.json
        doctor_object_id = ObjectId(doctor_id)
        db_connection.doctor.find_one_and_update({"_id": doctor_object_id}, {
            "$set": dict(doctor_data)
        })
        updated_doctor = doctor_entity(db_connection.doctor.find_one({"_id": doctor_object_id}))
        return response.json({"Details Updated": updated_doctor, "message": "Doctor Updated Successfully"}, status=200)

    except ValueError:
        return response.json({"message": "Incorrect Id"})
