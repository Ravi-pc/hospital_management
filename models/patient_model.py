def patient_entity(item) -> dict:
    return {
        "id": str(item['_id']),
        "name": item.get('name', ''),
        "age": item.get('age', ''),
        "sex": item.get('sex', ''),
        "medical_history": item.get('medical_history', ''),
        "contact": item.get('contact', '')
    }


def patients_entity(entity) -> list:
    return [patient_entity(item) for item in entity]
