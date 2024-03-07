from sanic import Sanic
from sanic.response import text
from routes.doctor_api import doctor_api

app = Sanic('HospitalManagement')

app.blueprint(doctor_api)

