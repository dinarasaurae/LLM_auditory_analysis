import requests
import csv
from config import access_token

group_id = '215205015'


def get_user_groups(user_id, access_token):
    """Получение списка групп пользователя с их названиями."""
    groups = []
    try:
        response = requests.get('https://api.vk.com/method/groups.get', params={
            'user_id': user_id,
            'extended': 1,  
            'access_token': access_token,
            'v': '5.131',
            'count': 40  
        }).json()
        if 'response' in response:
            groups = [group['name'] for group in response['response']['items']]
    except Exception as e:
        print(f"Ошибка при получении групп пользователя {user_id}: {e}")
    return groups

def get_user_careers(user_id, access_token):
    """Получение информации о должностях в карьере пользователя."""
    careers_positions = ''
    try:
        response = requests.get('https://api.vk.com/method/users.get', params={
            'user_ids': user_id,
            'fields': 'career',
            'access_token': access_token,
            'v': '5.131'
        }).json()
        if 'response' in response:
            user_data = response['response'][0]
            if 'career' in user_data and user_data['career']:
                # Собираем только должности из каждой записи карьеры
                positions = [career.get('position') for career in user_data['career'] if career.get('position')]
                careers_positions = '; '.join(positions)
    except Exception as e:
        print(f"Ошибка при получении информации о карьере пользователя {user_id}: {e}")
    return careers_positions

def get_user_interests(user_id, access_token):
   
    interests = ''
    try:
        response = requests.get('https://api.vk.com/method/users.get', params={
            'user_ids': user_id,
            'fields': 'personal',
            'access_token': access_token,
            'v': '5.131'
        }).json()
        if 'response' in response:
            user_data = response['response'][0]
            if 'personal' in user_data and 'interests' in user_data['personal']:
                interests = user_data['personal']['interests']
    except Exception as e:
        print(f"Ошибка при получении интересов пользователя {user_id}: {e}")
    return interests

def get_users(group_id, limit=8000):
    all_users = []
    fields = 'sex,bdate,city'
    count = 1000  # Максимальное количество пользователей за запрос
    offset = 3003 # Начальное смещение

    while len(all_users) < limit:
        params = {
            'access_token': access_token,
            'v': '5.131',
            'group_id': group_id,
            'fields': fields,
            'count': count,
            'offset': offset
        }
        response = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()
        users = response.get('response', {}).get('items', [])
        all_users.extend(users)
        offset += count  # Увеличиваем смещение для следующего запроса
        
        if len(users) < count:  # Проверка на последнюю страницу данных
            break

    with open('user_data_with_groups_activities_careers_3.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['sex', 'bdate', 'city', 'groups', 'careers'])
        
        for user in all_users:
            bdate = user.get('bdate', '')
            if bdate.count('.') == 2:
                formatted_bdate = bdate
            else:
                formatted_bdate = None
                
            sex = 'м' if user.get('sex') == 2 else 'ж' if user.get('sex') == 1 else None
            city = user.get('city', {}).get('title', '') if user.get('city') else None
            groups = '; '.join(get_user_groups(user['id'], access_token))
            careers = get_user_careers(user['id'], access_token)
            writer.writerow([sex, formatted_bdate, city, groups, careers])

get_users(group_id, limit=1000)
