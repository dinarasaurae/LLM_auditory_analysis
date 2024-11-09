import requests
import csv
import time
from config import access_token

group_id = '215205015'

def get_group_members(group_id, access_token): #  ID падпещеков
    members = []
    response = requests.get('https://api.vk.com/method/groups.getMembers', params={
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131'
    }).json()
    if 'response' in response:
        members = response['response']['items']
    return members

def get_user_groups(user_id, access_token):   #  список групп пользователя
    groups = []
    try:
        response = requests.get('https://api.vk.com/method/groups.get', params={
            'user_id': user_id,
            'extended': 0,
            'access_token': access_token,
            'v': '5.131'
        }).json()
        if 'response' in response:
            groups = response['response']['items']
    except Exception as e:
        print(f"Ошибка при получении групп пользователя {user_id}: {e}")
    return groups

def main():
    members = get_group_members(group_id, access_token)
    all_groups = {}

    for user_id in members:
        user_groups = get_user_groups(user_id, access_token)
        for group in user_groups:
            if group not in all_groups:
                all_groups[group] = 0
            all_groups[group] += 1
        time.sleep(0.5) 

    with open('groups.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID группы', 'Количество подписчиков'])
        for group, count in all_groups.items():
            writer.writerow([group, count])

if __name__ == '__main__':
    main()
