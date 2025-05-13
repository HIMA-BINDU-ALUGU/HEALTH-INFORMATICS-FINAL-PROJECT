import csv
import uuid
from datetime import datetime
from tkinter import messagebox

class Patient:
    def __init__(self, patient_data_file, notes_file):
        self.patient_data_file = patient_data_file
        self.notes_file = notes_file
        self.patients = self.load_data()

    def load_data(self):
        patients = {}
        try:
            with open(self.patient_data_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pid = row['Patient_ID']
                    if pid not in patients:
                        patients[pid] = []
                    patients[pid].append(row)
        except FileNotFoundError:
            print(f"Patient data file '{self.patient_data_file}' not found.")
        return patients

    def save_data(self):
        if not self.patients:
            return

        with open(self.patient_data_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = list(self.patients[list(self.patients.keys())[0]][0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for visits in self.patients.values():
                for visit in visits:
                    writer.writerow(visit)

    def add_patient(self, info_dict):
        pid = info_dict['Patient_ID']
        visit_id = str(uuid.uuid4())[:8]
        note_id = str(uuid.uuid4())[:8]

        info_dict['Visit_ID'] = visit_id
        info_dict['Note_ID'] = note_id

        if pid not in self.patients:
            self.patients[pid] = []
        self.patients[pid].append(info_dict)
        self.save_data()

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            self.save_data()
            return True
        return False

    def retrieve_patient(self, patient_id):
        return self.patients.get(patient_id, [])

    from datetime import datetime

    from datetime import datetime

    def count_visits(self, date_str):
        total = 0
        try:
            entered = datetime.strptime(date_str, "%Y-%m-%d").strftime("%#m/%#d/%Y")  # Use %-m/%-d/%Y on Linux/mac
        except ValueError:
            entered = date_str.strip()

        print("Comparing against entered date:", entered)

        for visits in self.patients.values():
            for visit in visits:
                visit_date = visit.get('Visit_time', '').strip()
                print(" - Found visit date:", visit_date)
                if visit_date == entered:
                    total += 1
        return total

    def view_note(self, patient_id, visit_date):
        print("Looking for Note for patient:", patient_id, "on date:", visit_date)

        if patient_id not in self.patients:
            print("Patient not found")
            return "Patient not found."

        note_id = None
        for visit in self.patients[patient_id]:
            print(" - visit date:", visit.get('Visit_time'), "| note ID:", visit.get('Note_ID'))
            if visit.get('Visit_time', '').strip() == visit_date.strip():
                note_id = visit.get('Note_ID')
                break

        if not note_id:
            return "Note ID not found for this date."

        try:
            with open(self.notes_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Note_ID'].strip() == note_id.strip():
                        return row['Note_text']
        except FileNotFoundError:
            return f"Notes file '{self.notes_file}' not found."

        return "Note not found."

