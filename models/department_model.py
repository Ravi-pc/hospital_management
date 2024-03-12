def department_entity(item) -> dict:
    return {
        "id": str(item['_id']),
        "department_name": item.get('department_name', ''),
        "description": item.get('description', ''),
        "head_of_department": item.get('head_of_department', ''),
        "number_of_staff": item.get('number_of_staff', ''),
        "capacity": item.get("capacity", ''),
        "contact": item.get('contact', '')
    }


def departments_entity(entity) -> list:
    return [department_entity(item) for item in entity]
