# data_for_3yrs.py
 
import csv
import random
import time
from datetime import datetime, timedelta
import nltk
 
nltk.download('words')
 
# List of possible values for role
roles = ['admin', 'api-user', 'end-user', 'db-user']
 
# Function to generate random search_type (hybrid or keyword)
def generate_search_type():
    return random.choice(['hybrid', 'keyword'])
 
# Function to generate random search_tag (random words from NLTK corpus)
def generate_search_tag():
    words = random.sample(nltk.corpus.words.words(), k=random.randint(1, 4))
    return ' '.join(words)
 
# Function to generate random date within the last 3 years
def generate_random_date():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 1, 1)
 
    time_difference = end_date - start_date
    random_days = random.randint(0, time_difference.days)
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime('%Y-%m-%d %H:%M:%S')
 
# Function to generate random data
def generate_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            'id': random.randint(1000, 9999),
            'search_type': generate_search_type(),
            'search_tag': generate_search_tag(),
            'role': random.choice(roles),
            'timestamp': generate_random_date(),
            'result_count': random.randint(1, 29),  
            'search_duration': round(random.uniform(0.5, 5.0), 2),
        }
        data.append(record)
    return data
 
def save_to_csv(data, filename='search_data.csv'):
    fieldnames = ['id', 'search_type', 'search_tag', 'role', 'timestamp', 'result_count', 'search_duration']
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for record in data:
            writer.writerow(record)
 
data = generate_data(1000)
save_to_csv(data)
 
print("3 years of data has been generated and saved to 'search_data.csv'.")
