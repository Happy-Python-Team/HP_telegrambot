import datetime
from io import BytesIO
import os

import aiohttp
from aiogram import types

from bot_configure import bot


id_admin = str(os.getenv('ADMIN'))


async def sql_read(state):

    async with state.proxy() as data:

        tg_id = data['tg_id']
        group_name = data['group_name']
        count = data['post_count']
        short_username = data['short_username']

        if int(count) > 500:
            await bot.send_message(tg_id,
                                   'Выгрузка большого количества постов вредит вашему здоровью ☠️ (с)Разработчик')
        if len(group_name) < 3:
            await bot.send_message(tg_id, '🚫 Слишком короткое имя')

        else:
            try:
                await parser(tg_id, group_name, count, short_username)

            except Exception as e:
                print(e)


async def iter_posts(posts):
    for post in posts:
        yield post


async def parser(tg_id, group_name, count, short_username):
    token = str(os.getenv('VK_TOKEN'))

    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={token}&v=5.131"
    check = f"https://api.vk.com/method/utils.resolveScreenName?access_token={token}&screen_name={group_name}&v=5.131"

    async with aiohttp.ClientSession() as session:
        async with session.get(check) as response:
            src_check = await response.json()

        if src_check['response']['type'] != 'group':
            await bot.send_message(tg_id, f'{group_name} не является сообществом. Мы против парсинга личных '
                                          f'страниц пользователей ⛔ ')
        else:
            is_subscriber_id_url = f"https://api.vk.com/method/utils.resolveScreenName?access_token={token}" \
                                   f"&screen_name={short_username}&v=5.131 "

        async with session.get(is_subscriber_id_url) as response:
            user_data = await response.json()
            user_id = user_data['response']['object_id']

        is_subscriber_check = f"https://api.vk.com/method/groups.isMember?access_token={token}" \
                              f"&group_id=happython&user_id={user_id}&v=5.131"

        async with session.get(is_subscriber_check) as response:

            rs = await session.get(url)
            src = await rs.json()
            json_src = await rs.read()

            fs = []

            fs.append({'stream': BytesIO(json_src)})

            posts = iter_posts(src["response"]["items"])

            is_subscriber = await response.json()
            media = types.MediaGroup()

            if is_subscriber['response'] == 1:
                await bot.send_message(tg_id,
                                       f'💟Вы подписчик нашего паблика. Спасибо вам за это! Для вас парсер '
                                       f'загрузит все картинки постов отдельно💟 ')

                stream_txt = ""

                async for post in posts:
                    stream_txt += post['text'] + '\r\n' + '***' + '\r\n'
                    post_id = post['id']

                    if "attachments" in post:
                        post = post["attachments"]

                        if post[0]["type"] == "photo":
                            for size in post[0]['photo']['sizes']:
                                if size['type'] == 'z':

                                    r = await session.get(size['url'])
                                    content = await r.read()

                                    media.attach_document(types.InputFile(BytesIO(content), filename=f'{post_id}.jpeg'))

                        if post[0].get('link'):
                            stream_txt += post[0]['link']['url'] + '\r\n' + '***' + '\r\n\r\n'

            else:
                await bot.send_message(tg_id, f'Подпишитесь на нашу группу ВК https://vk.com/happython и '
                                              f'откройте дополнительные возможности парсера 🐍 ')

        fs.append({'stream': BytesIO(stream_txt.encode())})

        await bot.send_message(id_admin, f'{tg_id} получил выдачу {datetime.date.today()} ')

        media.attach_document(types.InputFile(fs[0]['stream'], filename=f'{group_name}.json'))
        media.attach_document(types.InputFile(fs[1]['stream'], filename=f'{group_name}.txt'))

        for i in range(0, len(media.media), 10):
            await bot.send_media_group(tg_id, media=media.media[i:i+10])
