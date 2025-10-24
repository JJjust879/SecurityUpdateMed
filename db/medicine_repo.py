class MedicineRepo:
    def __init__(self, db_connection):
        self.conn = db_connection
        
    def get_all_medicine_names(self) -> list[str]:
        query = "SELECT name FROM medicine_info ORDER BY name ASC"
        result = self.conn.fetch_all(query)
        return [row[0] for row in result]
    
    def get_medicine_by_name(self, name):
        query = "SELECT * FROM medicine_info WHERE name = ?"
        return self.conn.fetch_one(query, (name,))

    def get_min_max_dosage(self, medicine_name: str) -> tuple[float, float] | None:
        query = "SELECT min_dosage, max_dosage FROM medicines_info WHERE name = ?"
        result = self.conn.fetch_one(query, (medicine_name,))
        
        if not result:
            return None
        
        return result[0], result[1]