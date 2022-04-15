import datetime
import json
import urllib.request
import requests
from bot_configure import bot
import shutil
import zipfile
import os
import sqlite3


async def sql_read(message, state):
    conn = sqlite3.connect('order.db')
    cur = conn.cursor()

    async with state.proxy() as data:
        try:

            tg_id = data['tg_id']
            group_name = data['group_name']
            count = data['post_count']
            short_username = data['short_username']
            if int(count) > 500:
                await bot.send_message(tg_id,
                                       'Выгрузка большого количества постов вредит вашему здоровью ☠️ (с)Разработчик')
            if len(group_name) < 3:
                await bot.send_message(tg_id,
                                       '🚫 Слишком короткое имя')
            else:
                cur.execute(
                    f"INSERT INTO orders(group_name,count,telegram_id,is_complete,short_username) VALUES(?,?,?,?,?);", (
                        str(group_name), str(count), str(tg_id), 'False', str(short_username)))
                conn.commit()
                await parser(cur=cur, con=conn)
        except Exception as e:
            await bot.send_message(1060217483, e)


def try_repeat(func):
    def wrapper(*args, **kwargs):
        count = 10

        while count:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print('Error:', e)
                count -= 1

    return wrapper


@try_repeat
async def parser(cur, con):
    token = os.getenv('VK_TOKEN')
    while True:

        result = cur.execute(f"SELECT * FROM orders WHERE is_complete = 'False'")

        data = result.fetchone()
        cur.execute(f"UPDATE orders SET is_complete = 'True' WHERE id = {data[0]}")
        con.commit()
        group_name = data[1]
        count = data[2]
        telegram_id = data[3]
        short_username = data[5]

        url = f"https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={token}&v=5.131"
        check = f"https://api.vk.com/method/utils.resolveScreenName?access_token={token}&screen_name={group_name}&v=5.131"
        check_control = requests.get(check)
        src_check = check_control.json()
        if src_check['response']['type'] != 'group':
            await bot.send_message(telegram_id, f'{group_name} не является сообществом. Мы против парсинга личных '
                                                f'страниц пользователей ⛔ ')
        else:
            req = requests.get(url)
            src = req.json()

            # проверяем существует ли директория с именем группы
            if os.path.exists(f"{group_name}"):
                pass
            else:
                os.mkdir(group_name)

            with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
                json.dump(src, file, indent=4, ensure_ascii=False)

            posts = src["response"]["items"]
            is_subscriber_id_url = f"https://api.vk.com/method/utils.resolveScreenName?access_token={token}" \
                                   f"&screen_name={short_username}&v=5.131 "
            user_data = requests.get(is_subscriber_id_url).json()
            user_id = user_data['response']['object_id']

            is_subscriber_check = f"https://api.vk.com/method/groups.isMember?access_token={token}" \
                                  f"&group_id=happython&user_id={user_id}&v=5.131"

            if requests.get(is_subscriber_check).json()['response'] == 1:
                await bot.send_message(telegram_id, f'💟Вы подписчик нашего паблика. Спасибо вам за это! Для вас парсер '
                                                    f'дополнительно загрузит все картинки постов отдельно💟 ')

                for post in posts:

                    post_id = post["id"]

                    try:
                        if "attachments" in post:
                            post = post["attachments"]
                            [urllib.request.urlretrieve(size['url'], f"{group_name}\{post_id}.jpeg") for size in
                             post[0]['photo']['sizes'] if post[0]["type"] == "photo" and size['type'] == 'z']
                            print('ok')

                    except Exception as e:
                        print(e)
            else:
                await bot.send_message(telegram_id, f'Подпишитесь на нашу группу ВК https://vk.com/happython и '
                                                    f'откройте дополнительные возможности парсера 🐍 ')

            z = zipfile.ZipFile(f'{group_name}.zip', 'w')  # Создание нового архива
            for root, dirs, files in os.walk(f'{group_name}'):  # Список всех файлов и папок в директории
                print(files)
                for file in files:
                    z.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив

            z.close()
            await bot.send_message(1060217483, f'{telegram_id} получил выдачу {datetime.date.today()} ')
            doc = open(f'{group_name}.zip', 'rb')
            print(doc)
            await bot.send_document(telegram_id, document=doc)
            cur.execute(f"UPDATE orders SET is_complete = 'True' WHERE id = {data[0]}")
            shutil.rmtree(group_name)
            os.remove(f'{group_name}.zip')
