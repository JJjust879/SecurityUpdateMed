from dataclasses import dataclass

@dataclass
class Dosage:
    illness: str
    medication: str
    dosage: int
    dosage_type: str
    times_per: str
    days_of_week: str
    frequency: str
    time: str
    date: str
    
    def to_tuple(self):
        return (
            self.illness,
            self.medication,
            f"{self.dosage} {self.dosage_type}",
            self.times_per,
            ', '.join(self.days_of_week.split(' ')),
            self.frequency,
            f"{self.date} {self.time}"
        )