# db/patient_repo.py

from models.patient import Patient
from utils.crypto import encrypt_str, decrypt_str

class PatientRepo:
    def __init__(self, db):
        self.db = db

    def get_all_patient_ids(self) -> list[str]:
        # Column name in DB is PatientID (case-insensitive anyway)
        query = "SELECT PatientID FROM patient_profile ORDER BY PatientID ASC"
        result = self.db.fetch_all(query)
        return [row[0] for row in result]

    def get_patient_profile(self, patient_id) -> Patient | None:
        """
        Load a patient profile from DB and transparently DECRYPT
        address and cp_no (phone number).
        """
        query = """
            SELECT PatientID, name, age, Birthdate, gender, address, cp_no
            FROM patient_profile
            WHERE PatientID = ?
        """
        result = self.db.fetch_one(query, (patient_id,))

        if not result:
            return None

        # result: (PatientID, name, age, Birthdate, gender, address, cp_no)
        decrypted_address = decrypt_str(result[5])
        decrypted_phone = decrypt_str(result[6])

        return Patient(
            patient_id=result[0],
            name=result[1],
            age=result[2],
            birthdate=result[3],
            gender=result[4],
            address=decrypted_address,
            cellphone_num=decrypted_phone,
        )

    # -------- OPTIONAL (future extension) --------

    def create_patient(self, patient: Patient):
        """
        Example: create a new patient with encrypted address and cp_no.
        Not used by current UI, but correct for future.
        """
        query = """
            INSERT INTO patient_profile
            (PatientID, name, age, Birthdate, gender, address, cp_no)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (
                patient.patient_id,
                patient.name,
                patient.age,
                patient.birthdate,
                patient.gender,
                encrypt_str(patient.address),
                encrypt_str(patient.cellphone_num),
            ),
        )

    def update_patient_contact(self, patient_id: str, new_address: str, new_phone: str):
        """
        Example: update encrypted contact information (address + cp_no).
        """
        query = """
            UPDATE patient_profile
            SET address = ?, cp_no = ?
            WHERE PatientID = ?
        """
        self.db.execute(
            query,
            (
                encrypt_str(new_address),
                encrypt_str(new_phone),
                patient_id,
            )
        )
