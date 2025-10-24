from dataclasses import dataclass

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    birthdate: str
    gender: str
    address: str
    cellphone_num: str