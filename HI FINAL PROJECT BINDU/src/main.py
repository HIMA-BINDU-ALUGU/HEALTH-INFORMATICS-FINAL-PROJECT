import tkinter as tk
from ui_app import AppUI

def main():
    root = tk.Tk()
    root.geometry("400x400")
    app = AppUI(
        root,
        credentials_path="../data/Credentials.csv",
        patient_path="../data/Patient_data.csv",
        notes_path="../data/Notes.csv"

    )
    root.mainloop()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
