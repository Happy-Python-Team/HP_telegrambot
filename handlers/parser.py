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

            token = os.getenv('VK_TOKEN')
            tg_id = data['tg_id']
            group_name = data['group_name']
            count = data['post_count']

            cur.execute(f"INSERT INTO orders(group_name,count,telegram_id,is_complete) VALUES(?,?,?,?);", (
                str(group_name), str(count), str(tg_id), 'False',))
            conn.commit()
            url = f"https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={token}&v=5.131"
            req = requests.get(url)
            src = req.json()

            # проверяем существует ли директория с именем группы
            if os.path.exists(f"{group_name}"):
                print(f"Директория с именем {group_name} уже существует!")
            else:
                os.mkdir(group_name)

            with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
                json.dump(src, file, indent=4, ensure_ascii=False)

            posts = src["response"]["items"]

            for post in posts:

                post_id = post["id"]

                try:
                    if "attachments" in post:
                        post = post["attachments"]
                        [urllib.request.urlretrieve(size['url'], f"{group_name}\{post_id}.jpeg") for size in
                         post[0]['photo']['sizes'] if post[0]["type"] == "photo" and size['type'] == 'z']


                except Exception as e:
                    print(e)

            z = zipfile.ZipFile(f'{group_name}.zip', 'w')  # Создание нового архива
            for root, dirs, files in os.walk(f'{group_name}'):  # Список всех файлов и папок в директории
                for file in files:
                    z.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив

            z.close()
            await bot.send_message(1060217483, f'{message.from_user.username} получил выдачу {datetime.date.today()} ')
            doc = open(f'{group_name}.zip', 'rb')
            print(doc)
            await bot.send_document(message.from_user.id, document=doc)
            shutil.rmtree(group_name)
            os.remove(f'{group_name}.zip')

        except Exception as e:
            await bot.send_message(1060217483, e)
