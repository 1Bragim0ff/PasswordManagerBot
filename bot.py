from assets.settings import Settings
from assets.database import Database

import telebot

bot = telebot.TeleBot(Settings.TOKEN)
db = Database()

data = {}
data_for_delete = {}

# {
#   'user_id': {
#       'url': {
#           'login': ...
#           'password': ...
#       }
#   }
# }


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.from_user.id,
    'Добро пожаловать в Safe Password Manager \n /add - Добавить новый аккаунт \n \
/show - Показать данные аккаунта \n /showa - Показать все аккаунты \n /del - Удалить данные аккаунта')


@bot.message_handler(commands=['add'])
def add(message):
    data[message.from_user.id] = {}
    bot.send_message(message.from_user.id,
    'Напишите URL сайта: ')
    bot.register_next_step_handler(message, add_url)
    db.create(f'user{message.from_user.id}')

def add_url(message):
    global user_url
    user_url = message.text
    data[message.from_user.id][message.text] = {}
    bot.send_message(message.from_user.id,
    'Напишите логин аккаунта: ')
    bot.register_next_step_handler(message, add_login)

def add_login(message):
    data[message.from_user.id][user_url]['login'] = message.text
    bot.send_message(message.from_user.id,
    'Напишите пароль от аккаунта: ')
    bot.register_next_step_handler(message, add_password)

def add_password(message):
    global user_url
    data[message.from_user.id][user_url]['password'] = message.text

    user_id = message.from_user.id
    user_url = user_url
    user_login = data[user_id][user_url]['login']
    user_password = data[user_id][user_url]['password']

    db.add(f'user{user_id}', user_url, user_login, user_password)

@bot.message_handler(commands=['show'])
def show(message):
    bot.send_message(message.from_user.id,
    'Напишите URL сайта: ')
    bot.register_next_step_handler(message, show_url)

def show_url(message):
    account_info = db.get(f'user{message.from_user.id}', message.text)
    if not account_info is None:
        bot.send_message(message.from_user.id,
        f'URL: {account_info[0]} | Login: {account_info[1]} | Pass: {account_info[2]}')
    else:
        bot.send_message(message.from_user.id,
        'В базе данных такого URL нет')

@bot.message_handler(commands=['showa'])
def showa(message):
    accounts_info = db.geta(f'user{message.from_user.id}')

    if not accounts_info is None:
        for account_info in accounts_info:
            bot.send_message(message.from_user.id,
            f'URL: {account_info[0]} | Login: {account_info[1]} | Pass: {account_info[2]}')
    else:
        bot.send_message(message.from_user.id,
            'База данных пустая')


@bot.message_handler(commands=['del'])
def delete(message):
    data_for_delete[message.from_user.id] = {}
    bot.send_message(message.from_user.id,
    'Напишите URL сайта: ')
    bot.register_next_step_handler(message, delete_url)

def delete_url(message):
    data_for_delete[message.from_user.id]['url'] = message.text
    bot.send_message(message.from_user.id,
    'Напишите логин аккаунта: ')
    bot.register_next_step_handler(message, delete_login)

def delete_login(message):
    data_for_delete[message.from_user.id]['login'] = message.text
    
    user_id = message.from_user.id
    user_url = data_for_delete[user_id]['url']
    user_login = data_for_delete[user_id]['login']

    if not db.delete(f'user{user_id}', user_url, user_login) is None:
        bot.send_message(user_id,
        f'Аккаунт {user_url} - {user_login} удалён')
    else:
        bot.send_message(user_id,
        f'Аккаунт {user_url} - {user_login} не найден')

bot.polling()