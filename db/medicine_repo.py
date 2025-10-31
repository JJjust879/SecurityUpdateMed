class MedicineRepo:
    def __init__(self, db):
        self.db = db
        
    def get_all_medicine_names(self) -> list[str]:
        query = "SELECT name FROM medicine_info ORDER BY name ASC"
        result = self.db.fetch_all(query)
        return [row[0] for row in result]
    
    def get_medicine_dosage_by_name(self, name):
        query = "SELECT dosage, typeofdosage FROM medicine_info WHERE name = ?"
        return self.db.fetch_one(query, (name,))

    def get_min_max_dosage(self, medicine_name: str) -> tuple[float, float] | None:
        query = "SELECT minimumdosage, maximumdosage FROM medicine_info WHERE name = ?"                
        result = self.db.fetch_one(query, (medicine_name,))
        
        if not result:
            return None
        
        return result[0], result[1]