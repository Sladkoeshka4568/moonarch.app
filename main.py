import requests
import json
from fake_useragent import UserAgent
import time
import telebot



today = time.time()
dt = time.strftime('%Y-%m-%d_%H.%M', time.localtime(today))
ua = UserAgent()
token = '5429272897:AAEambLvd2TsehQxfX5DoyKIXYLa_yS1TZc'


def get_data():
    data_miners = []
    headers = {
        'User-Agent': f'{ua.random}',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://moonarch.app/',
        'Version': '2.13.1',
        'Origin': 'https://moonarch.app',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'If-None-Match': 'W/339de-L2gyEdk7994SFr7BKvh1PIYJtX4',
    }

    params = {
        'full': '1',
    }

    response = requests.get('https://api.moonarch.app/1.0/miners/list', params=params, headers=headers).json()
    for item in response.get('miners'):
        item_telegram = item.get('telegram')
        item_mining_group = item.get('name')
        item_url = item.get('url')
        item_poo_coin_charts = item.get('token').get('address')
        item_token = item.get('token').get('symbol')
        item_contract_balance_chat = item.get('contract')
        item_audited = item.get('audit')
        item_fees = item.get('fees')
        item_sell_fees = item.get('sellFees')
        item_age = int((today - item.get('created')) / 86400)
        item_daily = item.get('rate')
        item_TVL = item.get('balance')
        item_evol_TVL = item.get('balance24')
        item_actions = item.get('plans')
        if item_actions is None:
            item_actions = 'Buy'
        else:
            item_actions = 'Invest'

        data_miners.append({
                'Telegram': item_telegram,
                'Mining_group': item_mining_group,
                'url': item_url,
                'poo_coin_charts': f'https://poocoin.app/tokens/{item_poo_coin_charts}',
                'Token': item_token,
                'contract_balance_chat': f'https://bscscan.com/address/{item_contract_balance_chat}#analytics',
                'contract_code': f'https://bscscan.com/address/{item_contract_balance_chat}',
                'Audited': item_audited,
                'Fees': item_fees,
                'Sell_Fees': item_sell_fees,
                'Age': f'{item_age}d',
                'Daily': item_daily,
                'TVL': item_TVL,
                'Evol_TVL': item_evol_TVL,
                'Actions': item_actions
        })
    with open(f'result_for_{dt}.json', 'w', encoding='utf-8') as file:
        json.dump(data_miners, file, indent=4, ensure_ascii=False)
    return f'result_for_{dt}.json'


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Get data', 'Newsletter')
        bot.send_message(message.chat.id, 'Make a choice!', reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text == 'Get data':
            bot.send_document(message.chat.id, open(get_data()))
        elif message.text == 'Newsletter':
            bot.send_message(message.chat.id, 'Enter the interval (an integer number) of minutes at which you want to receive data')
            @bot.message_handler(content_types=['text'])
            def message_input_step(message):
                global interval
                interval = message.text
                while True:
                    bot.send_document(message.chat.id, open(get_data(), 'rb'))
                    time.sleep(int(interval)*60)

            bot.register_next_step_handler(message, message_input_step)
    bot.polling()


def main():
    telegram_bot(token)


if __name__ == '__main__':
    main()
