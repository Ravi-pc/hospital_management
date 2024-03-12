from pydantic import BaseModel


class Department(BaseModel):
    department_name: str
    head_of_department: str
    description: str
    number_of_staff: str
    capacity: str
    contact: str
