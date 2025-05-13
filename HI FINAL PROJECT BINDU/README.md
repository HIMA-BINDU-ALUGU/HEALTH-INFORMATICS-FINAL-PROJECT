# Clinical Data Warehouse System

This is a Python-based graphical user interface (GUI) application for managing clinical patient data. It handles role-based access for operations such as adding, removing, retrieving patients, counting visits, viewing notes, and generating analytics. The application is developed using the Tkinter library for the user interface and Matplotlib for statistics.

## Features

* User authentication with multiple roles (admin, nurse, clinician, management)
* Management users can:

  * Generate key statistics
  * View charts: visits over time, gender distribution, and insurance trend
* Admin users can:

  * Count visits on a specific date
* Nurse and clinician users can:

  * Retrieve patient visits by Patient ID
  * Add new patient records
  * Remove patient records
  * Count visits on a specific date
  * View notes associated with patient visits
* Usage logging with timestamped action history
## Files

* ui_app.py: GUI logic including role-specific menu options
* main.py: Program entry point; launches the application
* user.py: Handles login authentication and user role setup
* patient.py: Manages patient operations (add/remove/retrieve/count)
* note.py: Accesses and retrieves clinical note details
* records.py: Contains shared logic used by nurse/clinician roles
* statistics.py: Generates analytics and stores output charts
* logger.py: Logs user actions and statuses to usage\_log.csv
* data/Credentials.csv: Stores username, password, and role info
* data/Patient\_data.csv: Stores all visit-related patient data
* data/Notes.csv: Contains clinical notes linked to Patient\_ID and Visit\_ID
* output/usage\_log.csv: Auto-generated log file with each user interaction
* output/\*.png: Generated charts for management (statistics)
* UML\_diagram.png: System architecture and class interaction diagram
* requirements.txt: Python libraries needed to run the app

## Prerequisites

* Python 3.x
* Required libraries: tkinter, pandas, matplotlib, csv, datetime, uuid, os

## Usage

1. Ensure the following files are available in the correct folders:

   * src/: main.py, ui\_app.py, other .py modules
   * data/: Credentials.csv, Patient\_data.csv, Notes.csv
2. Open a terminal and run the application from src directory:

   ```
   python main.py
   ```
3. When prompted, log in using your username and password from Credentials.csv.
4. The menu will update based on your role (e.g., nurse, admin, etc.).
5. Follow on-screen prompts to perform actions like:

   * Add/Remove/Retrieve patients
   * Count visits by date
   * View note by Patient\_ID and Visit\_ID
   * Generate statistics if logged in as management
6. All user actions will be logged in output/usage\_log.csv

## Notes

* Credentials.csv should follow the format: username,password,role
* Patient\_data.csv should contain headers such as:
  Patient\_ID, Visit\_ID, Visit\_time, Visit\_department, Gender, Age, Insurance, ...
* Notes.csv should contain: Note\_ID, Patient\_ID, Visit\_ID, Note\_type, Note\_text
* Graphs will be saved to /output when generated


