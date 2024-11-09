import csv
import requests
import datetime
from config import access_token

version = 5.199
domain = 'midjourney'

def take_posts_by_date(start_date, end_date):
    all_posts = []
    start_unixtime = int(datetime.datetime.strptime(start_date, "%d.%m.%Y").timestamp())
    end_unixtime = int(datetime.datetime.strptime(end_date, "%d.%m.%Y").timestamp())

    for offset in range(0, 2000, 100): 
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': access_token,
                                    'v': version,
                                    'domain': domain,
                                    'count': 100,
                                    'offset': offset
                                }
                                )
        data = response.json()['response']['items']
        
        
        for post in data:
            if start_unixtime <= post['date'] <= end_unixtime:
                all_posts.append(post)
            elif post['date'] < start_unixtime:
                return all_posts  

    return all_posts

def file_writer(data):
    with open('datamining.csv', 'w', newline='', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'comments', 'views', 'reposts', 'text', 'date', 'time', 'attachments'))
        for post in data:
            attachments_count = len(post.get('attachments', []))
            time = datetime.datetime.fromtimestamp(post.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S')
            a_pen.writerow((post['likes']['count'], post['comments']['count'], post['views'].get('count', 'N/A'), post['reposts']['count'], post.get('text', ''), post.get('date', ''), time, attachments_count))

start_date = "01.01.2023"
end_date = "01.01.2024"
data = take_posts_by_date(start_date, end_date)
file_writer(data)
