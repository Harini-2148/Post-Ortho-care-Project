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

# Function to save data to a log file
def save_to_log(data, filename='search_data.log'):
    with open(filename, mode='w') as file:
        for record in data:
            log_entry = (
                f"[{record['timestamp']}] ID: {record['id']}, "
                f"Role: {record['role']}, Search Type: {record['search_type']}, "
                f"Tag: '{record['search_tag']}', Result Count: {record['result_count']}, "
                f"Duration: {record['search_duration']}s\n"
            )
            file.write(log_entry)

# Generate and save data
data = generate_data(1000)
save_to_log(data)

print("3 years of data has been generated and saved to 'search_data.log'.")

