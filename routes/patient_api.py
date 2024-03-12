from pymongo.errors import DuplicateKeyError
from sanic import Blueprint, response
from sanic_ext.extensions.openapi import openapi
from sanic.exceptions import NotFound
from config.db import db_connection
from models.doctor_model import doctor_entity, doctors_entity
from models.patient_model import patients_entity, patient_entity
from schema.doctor_schema import Doctor
from bson import ObjectId

from schema.patient_schema import Patient

patient_api = Blueprint('patient', url_prefix='Patient')


@patient_api.get('/')
async def get_all_patients(request):
    patients = patients_entity(db_connection.local.patient.find())
    if not patients:
        raise NotFound("Database is empty")
    return response.json(patients)


@patient_api.post('/')
@openapi.definition(body={'application/json': Patient.model_json_schema()})
async def register_patient(request):
    patient_data = request.json
    try:
        user_id = db_connection.local.patient.insert_one(dict(patient_data)).inserted_id
        user = db_connection.local.patient.find_one({"_id": user_id})
        return response.json({"message": 'User Added Successfully', 'user': patient_entity(user)}, status=201)
    except DuplicateKeyError:
        return response.json({"error": "User already exists"}, status=409)


@patient_api.delete('/delete_patient/<patient_id:str>')
async def delete_doctor(request, patient_id):
    try:
        patient_object_id = ObjectId(patient_id)
        deleted_patient = patient_entity(db_connection.local.patient.find_one_and_delete({"_id": patient_object_id}))
        if deleted_patient:
            return response.json({"deleted_patient": deleted_patient, "message": "Patient deleted successfully"})
        else:
            return response.json({"message": "Patient not found"}, status=404)

    except FileNotFoundError:
        return response.json({"message": "Incorrect _id"}, status=404)


@patient_api.put('/update/<patient_id:str>')
@openapi.definition(body={'application/json': Patient.model_json_schema()})
async def update_patient(request, patient_id):
    patient_data = request.json
    patient_object_id = ObjectId(patient_id)
    db_connection.local.patient.find_one_and_update({"id": patient_object_id}, {
        "$set": dict(patient_data)
    })
    # updated_doctor = doctor_entity(db_connection.local.doctor.find_one({"_id": patient_object_id}))
    return response.json({"message": "Doctor Updated Successfully"}, status=200)
