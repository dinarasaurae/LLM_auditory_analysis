import requests
import csv
from config import access_token 

def get_users(group_id, limit=20):

    all_users = []
    fields = 'sex,bdate,city'
    params = {
        'access_token': access_token, 'v': 5.131, 'group_id': group_id,
        'fields': fields, 'count': limit
    }
    response = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()
    users = response.get('response', {}).get('items', [])
    all_users.extend(users)

    filtered_users = []
    for user in all_users:
        bdate = user.get('bdate', '')
        if bdate.count('.') == 2:
            formatted_bdate = bdate
        else:
            formatted_bdate = None   
        filtered_user = {
            'sex': 'м' if user.get('sex') == 2 else 'ж' if user.get('sex') == 1 else None,
            'bdate': formatted_bdate,
            'city': user.get('city', {}).get('title', '') if user.get('city') else None
        }
        filtered_users.append(filtered_user)

    with open('user_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['sex', 'bdate', 'city'])
        writer.writeheader()
        for user in filtered_users:
            writer.writerow(user)

group_id = '215205015'
get_users(group_id, limit=20)
