from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    age: int
    sex: str
    medical_history: str
    contact: str

