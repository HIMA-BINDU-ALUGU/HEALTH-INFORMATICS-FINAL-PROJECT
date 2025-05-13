import tkinter as tk
from tkinter import messagebox, simpledialog
from user import UserManager
from patient import Patient
from statistics import StatsGenerator
from logger import UsageLogger

class AppUI:
    def __init__(self, root, credentials_path, patient_path, notes_path):
        self.root = root
        self.root.title("Clinical Data Warehouse")
        self.credentials_path = credentials_path
        self.patient_path = patient_path
        self.notes_path = notes_path

        self.user_manager = UserManager(credentials_path)
        self.logger = UsageLogger()
        self.patient_manager = Patient(patient_path, notes_path)

        self.current_user = None
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username").grid(row=0, column=0)
        tk.Label(self.root, text="Password").grid(row=1, column=0)

        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_manager.authenticate(username, password)

        if not user:
            self.logger.log_failed_login(username)
            messagebox.showerror("Error", "Invalid credentials.")
            return

        self.current_user = user
        self.logger.log(user.username, user.role, "Login")
        self.show_menu()

    def show_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome {self.current_user.username}!").pack()

        role = self.current_user.role
        if role in ['nurse', 'clinician']:
            options = [
                ("Add Patient", self.add_patient_ui),
                ("Remove Patient", self.remove_patient_ui),
                ("Retrieve Patient", self.retrieve_patient_ui),
                ("Count Visits", self.count_visits_ui),
                ("View Note", self.view_note_ui),
                ("Exit", self.root.quit)
            ]
        elif role == 'admin':
            options = [("Count Visits", self.count_visits_ui), ("Exit", self.root.quit)]
        elif role == 'management':
            options = [("Generate Statistics", self.generate_statistics_ui), ("Exit", self.root.quit)]

        for text, func in options:
            tk.Button(self.root, text=text, width=30, command=func).pack(pady=5)

    def add_patient_ui(self):
        data = self.prompt_patient_info()
        if data:
            self.patient_manager.add_patient(data)
            self.logger.log(self.current_user.username, self.current_user.role, "Add Patient")
            messagebox.showinfo("Success", "Patient added.")

    def remove_patient_ui(self):
        pid = simpledialog.askstring("Input", "Enter Patient ID to remove:")
        if pid:
            success = self.patient_manager.remove_patient(pid)
            action = "Remove Patient"
            self.logger.log(self.current_user.username, self.current_user.role, action)
            if success:
                messagebox.showinfo("Removed", "Patient removed.")
            else:
                messagebox.showwarning("Not Found", "Patient ID not found.")

    def retrieve_patient_ui(self):
        pid = simpledialog.askstring("Input", "Enter Patient ID to retrieve:")
        if pid:
            data = self.patient_manager.retrieve_patient(pid)
            self.logger.log(self.current_user.username, self.current_user.role, "Retrieve Patient")
            if data:
                result = "\n\n".join([f"{k}: {v}" for visit in data for k, v in visit.items()])
                messagebox.showinfo("Patient Info", result)
            else:
                messagebox.showwarning("Not Found", "Patient not found.")

    from datetime import datetime

    def count_visits_ui(self):
        from tkinter import simpledialog, messagebox
        date = simpledialog.askstring("Input", "Enter Date (YYYY-MM-DD):")
        if date:
            print("Entered date:", date)  # optional debug
            count = self.patient_manager.count_visits(date)
            print("Visit count returned:", count)  # optional debug
            self.logger.log(self.current_user.username, self.current_user.role, "Count Visits")
            messagebox.showinfo("Visit Count", f"{count} visit(s) found on {date}")

    def view_note_ui(self):
        pid = simpledialog.askstring("Input", "Enter Patient ID:")
        date = simpledialog.askstring("Input", "Enter Visit Date (YYYY-MM-DD):")
        if pid and date:
            note = self.patient_manager.view_note(pid, date)
            self.logger.log(self.current_user.username, self.current_user.role, "View Note")
            messagebox.showinfo("Clinical Note", note)


    def generate_statistics_ui(self):
        stats = StatsGenerator(self.patient_path)
        stats.visits_over_time()
        stats.insurance_trend()
        stats.gender_trend()
        self.logger.log(self.current_user.username, self.current_user.role, "Generate Statistics")
        messagebox.showinfo("Done", "Charts generated in output folder.")

    def prompt_patient_info(self):
        fields = [
            "Patient_ID", "Visit_time", "Visit_department", "Gender",
            "Race", "Ethnicity", "Age", "Zip_code", "Insurance",
            "Chief_complaint", "Note_type"
        ]
        data = {}
        for field in fields:
            val = simpledialog.askstring("Input", f"Enter {field.replace('_', ' ')}:")
            if not val:
                return None
            data[field] = val
        return data

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
