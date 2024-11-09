import requests
import csv
from config import access_token

group_id = '215205015'

import requests

def get_group_members(group_id, access_token):
    """Получение списка ID участников группы."""
    api_url = "https://api.vk.com/method/groups.getMembers"
    offset = 0
    members = []
    try:
        while True:
            params = {
                'group_id': group_id,
                'access_token': access_token,
                'v': '5.131',
                'offset': offset
            }
            response = requests.get(api_url, params=params).json()
            data = response.get('response', {})
            members.extend(data.get('items', []))
            # Проверяем, есть ли еще данные для получения
            if offset >= data.get('count', 0):
                break
            offset += 1000  # Максимальное количество участников, возвращаемых за один запрос, составляет 1000
    except Exception as e:
        print(f"Ошибка при получении участников группы: {e}")
    return members

def get_user_groups_with_activity(user_id, access_token):
    """Получение списка групп пользователя с названиями и тематиками."""
    groups_info = []
    try:
        response = requests.get('https://api.vk.com/method/groups.get', params={
            'user_id': user_id,
            'extended': 1,
            'fields': 'name,activity',
            'access_token': access_token,
            'v': '5.131',
            'count': 20
        }).json()
        if 'response' in response:
            for group in response['response']['items']:
                group_info = {
                    'user_id': user_id,
                    'group_name': group.get('name'),
                    'activity': group.get('activity', 'Не указана')
                }
                groups_info.append(group_info)
    except Exception as e:
        print(f"Ошибка при получении групп пользователя {user_id}: {e}")
    return groups_info

def create_normalized_groups_csv(group_id, access_token, limit=20):
    users = get_group_members(group_id, access_token)[:limit] 
    all_groups_info = []

    for user_id in users:
        user_groups = get_user_groups_with_activity(user_id, access_token)
        all_groups_info.extend(user_groups)

    # Создание CSV-файла
    with open('normalized_groups_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'group_name', 'activity'])
        writer.writeheader()
        for group_info in all_groups_info:
            writer.writerow(group_info)

# Вызов функции для создания файла
create_normalized_groups_csv(group_id, access_token)

