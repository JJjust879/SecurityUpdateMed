from models.dosage import Dosage


class DosageRepo:
    def __init__(self, db):
        self.db = db

    def get_dosages_by_patient(self, patient_id):
        query = """
            SELECT * FROM patient_dosage
            WHERE patientid = ?
        """
        rows = self.db.fetch_all(query, (patient_id,))
        dosages = []
        
        for row in rows:
            dosage = Dosage(
                illness=row[1],
                medication=row[2],
                dosage=row[3],
                dosage_type=row[4],
                times_per=row[5],
                days_of_week=row[6],
                frequency=row[7],
                time=row[8],
                date=row[9]
            )
            dosages.append(dosage)
        return dosages
    
    def insert_dosage(self, patient_id, medicine, dosage, dosagetype, timesper, date):
        query = """
                INSERT INTO patient_dosage
                (patientid, illness, medicine, dosage, dosagetype, timesper, daysoftheweek, 
                frequency, time, date)
                VALUES (?, 'General', ?, ?, ?, 'Day', 'N/A', 'N/A', ?, ?)
                """
        self.db.execute(query, (patient_id, medicine, dosage, dosagetype, timesper, date))
        
    def update_dosage(self, patient_id, medicine, new_dosage, new_dosagetype):
        query = """
            UPDATE patient_dosage SET dosage = ?, dosagetype = ? WHERE patientid = ? 
            AND medicine = ?
        """
        self.db.execute(query, (new_dosage, new_dosagetype, patient_id, medicine))