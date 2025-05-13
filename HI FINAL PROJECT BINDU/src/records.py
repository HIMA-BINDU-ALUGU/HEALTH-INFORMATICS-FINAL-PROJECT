import csv
import uuid
import os

class Visit:
    def __init__(self, visit_time, visit_department, chief_complaint, note_type, visit_id=None, note_id=None):
        self.visit_id = visit_id or str(uuid.uuid4())[:8]
        self.visit_time = visit_time
        self.visit_department = visit_department
        self.chief_complaint = chief_complaint
        self.note_id = note_id or str(uuid.uuid4())[:8]
        self.note_type = note_type

    def to_dict(self, patient_id, base_info):
        return {
            "Patient_ID": patient_id,
            "Visit_ID": self.visit_id,
            "Visit_time": self.visit_time,
            "Visit_department": self.visit_department,
            "Gender": base_info["Gender"],
            "Race": base_info["Race"],
            "Ethnicity": base_info["Ethnicity"],
            "Age": base_info["Age"],
            "Zip_code": base_info["Zip_code"],
            "Insurance": base_info["Insurance"],
            "Chief_complaint": self.chief_complaint,
            "Note_ID": self.note_id,
            "Note_type": self.note_type
        }

class PatientRecord:
    def __init__(self, patient_id, gender, race, ethnicity, age, zip_code, insurance):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.ethnicity = ethnicity
        self.age = age
        self.zip_code = zip_code
        self.insurance = insurance
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def to_dicts(self):
        base = {
            "Gender": self.gender,
            "Race": self.race,
            "Ethnicity": self.ethnicity,
            "Age": self.age,
            "Zip_code": self.zip_code,
            "Insurance": self.insurance
        }
        return [visit.to_dict(self.patient_id, base) for visit in self.visits]

class HospitalRecords:
    def __init__(self, filepath):
        self.filepath = filepath
        self.patients = self.load()

    def load(self):
        patients = {}
        if not os.path.exists(self.filepath):
            return patients

        with open(self.filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pid = row['Patient_ID']
                if pid not in patients:
                    patients[pid] = PatientRecord(
                        pid,
                        row['Gender'],
                        row['Race'],
                        row['Ethnicity'],
                        row['Age'],
                        row['Zip_code'],
                        row['Insurance']
                    )
                visit = Visit(
                    row['Visit_time'],
                    row['Visit_department'],
                    row['Chief_complaint'],
                    row['Note_type'],
                    row['Visit_ID'],
                    row['Note_ID']
                )
                patients[pid].add_visit(visit)
        return patients

    def save(self):
        if not self.patients:
            return
        all_rows = []
        for record in self.patients.values():
            all_rows.extend(record.to_dicts())
        with open(self.filepath, 'w', newline='', encoding='utf-8') as file:
            fieldnames = list(all_rows[0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)

    def count_visits_on_date(self, date):
        count = 0
        for record in self.patients.values():
            for visit in record.visits:
                if visit.visit_time == date:
                    count += 1
        return count
