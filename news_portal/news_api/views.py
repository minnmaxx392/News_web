from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
import csv
import requests
import pandas as pd
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

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def callAPI(keyword, category, area, language, depth):
    url = "https://api.dataforseo.com/v3/serp/google/news/live/advanced"
    text = keyword
    payload = '[{{"keyword":"{}", "location_code":{}, "language_code":"{}", "device":"desktop", "os":"windows", "depth":{}}}]'
    formatted_payload = payload.format(text, area, language, depth).encode()
    headers = {
        'Authorization': 'Basic bWluaDMwMDkwMkBnbWFpbC5jb206NGY4NGNiNTY4MWFhMWJmMA==',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=formatted_payload)

    save_json(response.json(), 'data_test.json')

def prepare_data():
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

def filter_data_trending(depth):
    # Đường dẫn tới file CSV của bạn
    csv_file_path = r'data_res.csv'

    # Khởi tạo danh sách để lưu trữ dữ liệu từ CSV
    data_list = []

    # Đọc dữ liệu từ file CSV và thêm nó vào danh sách
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data_list.append({
                'url': row['url'],
                'image_url': row['image_url'],
                'title': row['title'],
                'snippet': row['snippet'],
                'domain': row['domain'],
                'time_published': row['time_published'],
            })
    # Tạo context dựa trên dữ liệu từ CSV
    context = {'api_data': data_list[:depth]}
    # Render template và trả về nội dung HTML
    return context

def filter_data_new(depth):
    # Đường dẫn tới file CSV của bạn

    df = pd.read_csv('data_res.csv')
    # Khởi tạo danh sách để lưu trữ dữ liệu từ CSV
    
    # Chuyển đổi cột timestamp sang kiểu dữ liệu datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sắp xếp DataFrame theo cột timestamp
    df = df.sort_values(by='timestamp', ascending=False)

    # Lưu DataFrame đã sắp xếp vào file CSV mới
    df.to_csv('data_sorted.csv', index=False)

    data_list = []
    # Đọc dữ liệu từ file CSV và thêm nó vào danh sách
    with open('data_sorted.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data_list.append({
                'url': row['url'],
                'image_url': row['image_url'],
                'title': row['title'],
                'snippet': row['snippet'],
                'domain': row['domain'],
                'time_published': row['time_published'],
            })
    # Tạo context dựa trên dữ liệu từ CSV
    context = {'api_data': data_list[:depth]}

    # Render template và trả về nội dung HTML
    return context


def search(request):
    if request.method == 'POST':
        sort = request.POST.get('sort')
        keyword = request.POST.get('keyword')
        category = request.POST.get('category')
        area = request.POST.get('area')
        language = request.POST.get('language')
        depth = request.POST.get('count')
        # Xử lý dữ liệu ở đây
        try:
            callAPI(keyword, category, area, language, 100)
            prepare_data()
            if sort == "newnews":
                context = filter_data_new(int(depth))
            else:
                context = filter_data_trending(int(depth))
        except:
            context = {'api_data':
                       [{
                            'url': None,
                            'image_url': None,
                            'title': "Không tìm thấy bào báo theo yêu cầu",
                            'snippet': None,
                            'domain': None,
                            'time_published': None,
                       }]}
        return render(request, 'pages/index.html', context)

    return render(request, 'pages/index.html')  # Render form nếu không phải POST request

def reset_page(request):
    context = {}
    return render(request, 'pages/index.html', context)

def index(request):
    return render(request, 'pages\index.html')
