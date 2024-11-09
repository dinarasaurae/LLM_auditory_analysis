import csv
import requests
import datetime
import time  # Для задержки между запросами
from config import access_token

version = 5.199
domain = 'midjourney'

def take_posts_by_date(start_date, end_date):
    all_posts = []
    start_unixtime = int(datetime.datetime.strptime(start_date, "%d.%m.%Y").timestamp())
    end_unixtime = int(datetime.datetime.strptime(end_date, "%d.%m.%Y").timestamp())

    offset = 0
    while True:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': access_token,
                                    'v': version,
                                    'domain': domain,
                                    'count': 100,
                                    'offset': offset
                                })
        data = response.json()['response']['items']
        
        # Проверяем, если посты закончились
        if not data:
            break
        
        for post in data:
            if start_unixtime <= post['date'] <= end_unixtime:
                all_posts.append(post)
            elif post['date'] < start_unixtime:
                return all_posts  # Выходим, если дата поста меньше начальной даты
        
        offset += 0  # Увеличиваем смещение для следующего запроса
        time.sleep(0.5)  # Задержка для соблюдения лимитов API

    return all_posts

def file_writer(data):
    with open('vk_posts_1.csv', 'w', newline='', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'comments', 'views', 'reposts', 'text', 'date', 'time', 'attachments'))
        for post in data:
            attachments_count = len(post.get('attachments', []))
            time_str = datetime.datetime.fromtimestamp(post.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S')
            a_pen.writerow((post['likes']['count'], post['comments']['count'], post['views'].get('count', 'N/A'), post['reposts']['count'], post.get('text', ''), post.get('date', ''), time_str, attachments_count))

start_date = "01.01.2022"
end_date = "01.01.2024"
data = take_posts_by_date(start_date, end_date)
file_writer(data)
