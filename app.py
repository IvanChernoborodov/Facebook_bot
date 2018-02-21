import sqlite3
import os, sys

from flask import Flask, request, g
# Библиотека для удобной отправки facebook сообщений
from pymessenger import Bot
# функция, которая возвращает котировки
from exchange import get_btc
# Функция для сохранения id в файле
from searching import searching

# Здесь хранится токен для приложения
from secret import *




app = Flask(__name__)



bot = Bot(PAGE_ACCESS_TOKEN)


# Тестовая проверка на работоспособность сервера через GET запрос
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200




# Это наш webhook
@app.route('/', methods=['POST'])
def webhook():

    # Получаем информацию о сообщении и парсим ее
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                #IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):

                    if 'text' in messaging_event['message']:
                        # главная проверка
                        if messaging_event['message']['text'] == '/currency':
                            messaging_text = get_btc() + 'Ваш id= ' + sender_id + '' + ' Ваша чат группа= ' + recipient_id + '' + ' будут записаны в базу данных SQL'
                            # Если id пользователя нет в file.txt - записываем, если есть - пропускаем
                            searching(sender_id + os.linesep, 'file.txt')
                        else:
                            messaging_text = 'please enter /currency'


                    # ответ
                    response = messaging_text
                    # функция, которая посылает ответ
                    bot.send_text_message(sender_id, response)



    # Дефолт значение, статус http должен быть 200, чтобы работало корректно
    return "ok", 200



# Логируем сообщение для удобного просмотра
def log(message):
    print(message)
    sys.stdout.flush()


# Flask будет запускать в дебаг режиме на 80 порту
if __name__ == '__main__':
    app.run(debug= True , port = 80)