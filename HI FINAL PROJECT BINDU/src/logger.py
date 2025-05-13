import csv
from datetime import datetime
import os

class UsageLogger:
    def __init__(self, log_file='./output/usage_log.csv'):
        self.log_file = log_file
        self.init_log()

    def init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Username', 'Role', 'Action', 'Status'])

    def log(self, username, role, action, success=True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = 'Success' if success else 'Failed'
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, username, role, action, status])

    def log_failed_login(self, username):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, username, 'N/A', 'Login Attempt', 'Failed'])
