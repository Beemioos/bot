from bs4 import BeautifulSoup as bs
import requests
import telebot
from telebot import types
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

b_url = 'https://volit.ru/p/2784'


def parser():
    global all,groups, pars, auds,predmety
    session = requests.Session()
    request = session.get(b_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, "lxml")
        table = soup.find('table')

        groups = table.find_all('td', attrs={'width': '113'})

        pars = table.find_all('td', attrs={'width': '57'})

        auds = table.find_all('td', attrs={'width': '66'})

        predmety = table.find_all('td', attrs={'width': '340'})
    return groups, pars, auds,predmety
parser()


def cleaning():
    # группа
    groupp = {}

    for group, value in enumerate(groups):
        groupp[group] = value.text
    groupp.pop(0)

    # Кабинет
    audd = {}

    for aud, value1 in enumerate(auds):
        audd[aud] = value1.text
    audd.pop(0)
    # предмет
    predmett = {}

    for predmet, value1 in enumerate(predmety):
        predmett[predmet] = value1.text
    predmett.pop(0)
    # пара
    paraa = {}

    for para, value1 in enumerate(pars):
        paraa[para] = value1.text
    paraa.pop(0)
    # output
    allss = {}
    for (key1, value1), (key2, value2), (key3, value3), (key4,value4) in zip(groupp.items(), paraa.items(), predmett.items(),audd.items()):
        if paraa.keys() == predmett.keys():
            allss[value1] = ('Номер:' + value2, 'Пара:' + value3, 'Кабинет:' + str(value4))
    unique_dict = {key: (val[0].replace('\n', '-'), val[1].replace('\n', ','), val[2].replace('\n', ',')) for key, val in allss.items()}
    unique_dict = {key.replace('\n', ','): value for key, value in unique_dict.items()}
    print('Работа')
    global transformed_data
    transformed_data = {}
    for key, value in unique_dict.items():
        transformed_data[key] = {}
        for item in value:
            field, data = item.split(':')
            transformed_data[key][field] = data
cleaning()
# ////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////
token = '6525862222:AAGVG0abrXDhsjdfPtiIF36WaCfciRS72aI'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for group in transformed_data:
        btn = types.KeyboardButton(group)
        markup.add(btn)
    bot.send_message(message.chat.id, "Выберите группу:", reply_markup=markup)

# Обработчик выбора группы
@bot.message_handler(func=lambda message: True)
def show_schedule(message):
    if message.text in transformed_data:
        pairs = transformed_data[message.text]['Пара'].split(',')
        rooms = transformed_data[message.text]['Кабинет'].split(',')
        response = f"{message.text}\n"
        for i in range(len(pairs)):
            response += f"{transformed_data[message.text]['Номер'].split('-')[i]} {pairs[i]} {rooms[i]}\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Выберите группу из списка.")


bot.polling(none_stop=True)