
def doctor_entity(item) -> dict:
    return {
        "id": str(item['_id']),
        "first_name": item.get('first_name', ''),
        "last_name": item.get('last_name', ''),
        "department": item.get('department', ''),
        "contact": item.get('contact', ''),
    }


def doctors_entity(entity) -> list:
    return [doctor_entity(item) for item in entity]
