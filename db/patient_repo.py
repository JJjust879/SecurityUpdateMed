from models.patient import Patient

class PatientRepo:
    def __init__(self, db):
        self.db = db

    def get_all_patient_ids(self) -> list[str]:
        query = "SELECT patientid FROM patient_profile ORDER BY patientid ASC"
        result = self.db.fetch_all(query)
        return [row[0] for row in result]

    def get_patient_profile(self, patient_id) -> Patient | None:
        query = "SELECT * FROM patient_profile WHERE patientid = ?"
        result = self.db.fetch_one(query, (patient_id,))
        
        if not result:
            return None
        
        return Patient(
            patient_id=result[0],
            name=result[1],
            age=result[2],
            birthdate=result[3],
            gender=result[4],
            address=result[5],
            cellphone_num=result[6]
        )