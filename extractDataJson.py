import json
import csv

# Function to save data to a CSV file
def save_csv(data, filename):
    # Define the field names (column names) for your CSV
    fieldnames = [
        "rank_group",
        "rank_absolute",
        "domain",
        "title",
        "url",
        "image_url",
        "snippet",
        "time_published",
        "timestamp",
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        csv_writer.writeheader()

        # Write the data
        for item in data:
            csv_writer.writerow(item)

# Function to read a JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        return str(e)

# Testing the function with the provided JSON file
file_path = 'data_test.json'
json_content = read_json_file(file_path)

# Loop for each tasks
news_search_data = []

# Loop through each task
for task in json_content.get("tasks", []):
    # Check if 'result' exists in task and is a list
    if 'result' in task and isinstance(task['result'], list):
        # Loop through each result in the task
        for result in task['result']:
            # Check if the result type is "news_search"
            for item in result.get("items"):
                if item.get("type") == "news_search":
                    news_item = {
                        "rank_group": item.get("rank_group"),
                        "rank_absolute": item.get("rank_absolute"),
                        "domain": item.get("domain"),
                        "title": item.get("title"), 
                        "url": item.get("url"),
                        "image_url": item.get("image_url"),
                        "snippet": item.get("snippet"),
                        "time_published": item.get("time_published"),
                        "timestamp": item.get("timestamp"),
                    }
                    news_search_data.append(news_item)


# Save the data to a CSV file
save_csv(news_search_data, 'data_res.csv')
