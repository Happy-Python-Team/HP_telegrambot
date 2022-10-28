import datetime
import os

import aiohttp
"""
Парсер групп в Вконтакте (vk) по списку введенных групп
Данный парсер анализирует группы Вконтакте с целью выявления активных пользователей
Данная идея пришла при выборе группы для покупки рекламы,
ведь чем больше активной аудитории, тем выше будет охват рекламы в данной группе.

По всем возникшим вопросам, можете писать в группу https://vk.com/happython
"""
token_vk = str(os.getenv('VK_TOKEN'))


async def get_offset(group_id):
    """Выявляем параметр offset для групп, 1 смещение * 1000 id"""
    params = {'access_token': token_vk, 'group_id': group_id, 'v': 5.131}

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.vk.com/method/groups.getMembers', params=params) as response:
            count = await response.json()
            count = count['response']['count']
            print(f'Количество подписчиков: {count}')

            if count > 1000:
                count = count // 1000
            else:
                count = 1

    return count


async def vk_analyzer_run(group_id):

    last_30_days = datetime.datetime.now().date() - datetime.timedelta(days=30)
    count_active_users = 0
    count_users_can_closed_visit = 0

    try:
        count_subscribers = await get_offset(group_id['text'])

        for offset in range(0, count_subscribers+1):
            params = {'access_token': token_vk, 'v': 5.131, 'group_id': group_id['text'], 'offset': offset*1000, 'fields': 'last_seen'}

            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.vk.com/method/groups.getMembers', params=params) as response:
                    users = await response.json()
                    users = users['response']

                    for user in users['items']:
                        # проверка последнего посещения, не ранее указанной даты from_data преобразованной в timestamp
                        start_point_data = datetime.datetime.strptime(str(last_30_days), '%Y-%m-%d').timestamp()
                        try:
                            if user['last_seen']['time'] >= start_point_data:

                                count_active_users += 1

                        except:
                            count_users_can_closed_visit += 1

    except Exception as ex:
        return f'{group_id} - непредвиденная ошибка: {ex}\n'

    count_un_active_users = users["count"] - count_active_users
    text = f'Анализируем группу - {group_id["text"]} с {last_30_days}\nУчастников: {users["count"]}\n' \
           f'Количество пользователей со скрытой датой: {count_users_can_closed_visit}\n' \
           f'Активных подписчиков: {count_active_users} ({round((count_active_users / users["count"]) * 100, 2)}%)\n' \
           f'Не активные подписчики: {count_un_active_users}\n'

    return text