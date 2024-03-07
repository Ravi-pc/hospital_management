from pydantic import BaseModel


class Doctor(BaseModel):
    first_name: str
    last_name: str
    department: str
    contact: str
