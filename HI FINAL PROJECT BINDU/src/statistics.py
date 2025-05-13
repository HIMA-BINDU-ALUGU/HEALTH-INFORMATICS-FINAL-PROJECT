import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

class StatsGenerator:
    def __init__(self, patient_data_file):
        self.data_file = patient_data_file
        self.df = self.load_data()

    def load_data(self):
        try:
            df = pd.read_csv(self.data_file)
            return df
        except FileNotFoundError:
            print(f"Patient data file '{self.data_file}' not found.")
            return pd.DataFrame()

    def visits_over_time(self):
        if self.df.empty:
            return
        visits = self.df['Visit_time'].value_counts().sort_index()
        visits.plot(kind='bar', title='Visits Over Time', figsize=(10, 5))
        plt.xlabel('Date')
        plt.ylabel('Number of Visits')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('./output/visits_over_time.png')
        plt.close()

    def insurance_trend(self):
        if self.df.empty:
            return
        counts = self.df['Insurance'].value_counts()
        counts.plot(kind='pie', autopct='%1.1f%%', title='Insurance Type Distribution', figsize=(6, 6))
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('./output/insurance_trend.png')
        plt.close()

    def gender_trend(self):
        if self.df.empty:
            return
        counts = self.df['Gender'].value_counts()
        counts.plot(kind='bar', color='teal', title='Gender Distribution', figsize=(6, 4))
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig('./output/gender_trend.png')
        plt.close()
