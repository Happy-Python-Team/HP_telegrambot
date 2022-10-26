import os
from decimal import Decimal

import aiohttp


headers = {
    "Authorization": f"OAuth {str(os.getenv('YANDEX_TOKEN'))}"
}


async def parse_metrics_and_yandex_advertise_network(url, period=True, btn=""):
    text = ""

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            json = await response.json()

            points = json['data']['points']
            sorted_data_points = sorted(points, key=lambda item: item['dimensions']['date'][0])

            for i in range(0, len(sorted_data_points), 2):
                try:
                    payment_rtb_blocks = sorted_data_points[i+1]['measures'][0]['partner_wo_nds']
                    text += sorted_data_points[i]['dimensions']['date'][0] + "\n"
                    payment_recommendation_widget = sorted_data_points[i]['measures'][0]['partner_wo_nds']
                    text += f"Вознаграждение | Рекомендательный виджет: {payment_recommendation_widget}₽\n"
                    text += f"Вознаграждение | RTB-блоки: {payment_rtb_blocks}₽\n"
                    text += f"Всего: {Decimal(str(payment_recommendation_widget)) + Decimal(str(payment_rtb_blocks))}₽\n\n"

                except IndexError:
                    text += sorted_data_points[i]['dimensions']['date'][0] + "\n"

                    if sorted_data_points[i]['dimensions']['block_level'] == "RTB-блоки":
                        payment_rtb_blocks = sorted_data_points[i]['measures'][0]['partner_wo_nds']
                        text += f"Вознаграждение | RTB-блоки: {payment_rtb_blocks}₽\n"
                        text += f"Всего: {payment_rtb_blocks}₽\n\n"

                    else:
                        payment_recommendation_widget = sorted_data_points[i]['measures'][0]['partner_wo_nds']
                        text += f"Вознаграждение | Рекомендательный виджет: {payment_recommendation_widget}₽\n"
                        text += f"Всего: {payment_recommendation_widget}₽\n\n"

            if period:
                payment_mouth = json['data']['totals']['2'][0]['partner_wo_nds']

                if btn == "период":
                    text += f"\nВознаграждение за текущий период: {payment_mouth}₽\n"
                else:
                    text += f"\nВознаграждение за текущий месяц: {payment_mouth}₽\n"

                try:
                    average_payment = round(payment_mouth / (len(sorted_data_points) / 2), 2)
                except ZeroDivisionError:
                    average_payment = 0

                text += f"В среднем за день: {average_payment}₽"

    return text
