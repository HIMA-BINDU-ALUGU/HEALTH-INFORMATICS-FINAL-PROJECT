import csv

class NoteManager:
    def __init__(self, notes_file):
        self.notes_file = notes_file
        self.notes_dict = self.load_notes()

    def load_notes(self):
        notes_dict = {}
        try:
            with open(self.notes_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = (row['Patient_ID'].strip(), row['Visit_ID'].strip())
                    notes_dict[key] = {
                        "Note_ID": row["Note_ID"].strip(),
                        "Note_type": row["Note_type"],
                        "Note_text": row["Note_text"]
                    }
        except Exception as e:
            print(f"Error loading notes: {e}")
        return notes_dict

    def get_note_by_patient_and_visit(self, patient_id, visit_id):
        key = (patient_id.strip(), visit_id.strip())
        return self.notes_dict.get(key, {
            "Note_ID": "Unknown",
            "Note_type": "Unknown",
            "Note_text": f"Note not found for Patient {patient_id} and Visit {visit_id}"
        })
