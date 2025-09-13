from datetime import datetime

def get_current_date_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def calculate_duration_in_minutes(started_at, ended_at) -> float:
    # Define the format for parsing the datetime strings
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"
    
    # Convert the datetime strings to datetime objects
    start_time = datetime.strptime(started_at, datetime_format)
    end_time = datetime.strptime(ended_at, datetime_format)
    
    # Calculate the difference in minutes
    duration = (end_time - start_time).total_seconds() / 60
    
    return duration
