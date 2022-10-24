import requests
import datetime
import os
"""
Парсер групп в Вконтакте (vk) по списку введенных групп
Данный парсер анализирует группы Вконтакте с целью выявления активных пользователей
Данная идея пришла при выборе группы для покупки рекламы,
ведь чем больше активной аудитории, тем выше будет охват рекламы в данной группе.

По всем возникшим вопросам, можете писать в группу https://vk.com/happython
"""
token_vk = str(os.getenv('VK_TOKEN'))


def get_offset(group_id):
    """Выявляем параметр offset для групп, 1 смещение * 1000 id"""
    params = {'access_token': token_vk, 'group_id': group_id, 'v': 5.131}
    r = requests.get('https://api.vk.com/method/groups.getMembers', params=params)
    count = r.json()['response']['count']
    print(f'Количество подписчиков: {count}')
    if count > 1000:
        return count // 1000
    else:
        count = 1
        return count


def vk_analyzer_run(group_id):

    last_30_days = datetime.datetime.now().date() - datetime.timedelta(days=30)
    active_list = []
    users_can_closed_visit = []
    un_active_list = []
    try:
        for offset in range(0, get_offset(group_id)+1):
            params = {'access_token': token_vk, 'v': 5.131, 'group_id': group_id, 'offset': offset*1000, 'fields': 'last_seen'}
            users = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()['response']
            for user in users['items']:
                # проверка последнего посещения, не ранее указанной даты from_data преобразованной в timestamp
                start_point_data = datetime.datetime.strptime(str(last_30_days), '%Y-%m-%d').timestamp()
                try:
                    if user['last_seen']['time'] >= start_point_data:

                        active_list.append(user['id'])
                    else:
                        un_active_list.append(user['id'])
                except:
                    users_can_closed_visit.append(user['id'])

        text = f'Анализируем группу - {group_id["text"]} с {last_30_days}\nУчастников: {users["count"]}\n' \
               f'Количество пользователей со скрытой датой: {len(users_can_closed_visit)}\n' \
               f'Активных подписчиков: {len(active_list)} ({round(len(active_list) / (users["count"] - len(un_active_list)) *100, 2)}%)\n' \
               f'Не активные подписчики: {len(un_active_list)}\n'
        return text
    except Exception as ex:
        return f'{group_id} - непредвиденная ошибка: {ex}\n'


