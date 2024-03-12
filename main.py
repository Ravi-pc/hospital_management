from sanic import Sanic

from routes.department_api import department_api
from routes.doctor_api import doctor_api

app = Sanic('HospitalManagement')

app.blueprint(doctor_api)
app.blueprint(department_api)
