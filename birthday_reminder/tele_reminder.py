import telebot
from telebot import types


# token from telegram
bot=telebot.TeleBot("6235774110:AAFhV7WQ96YjqkvbRTl5-usGzPoue9lF4rU")

# dictionary to load into databse
data_dict = {
        "dan":2746,
        "mom":845
    }


@bot.message_handler(commands=['start'])

# congreeting messages
def start(message):

    text=f'hello, {message.from_user.first_name}, I\'m bot which will remind\
     you about birhdays'
    bot.send_message(message.chat.id,text ,parse_mode='html')

    text='What would you like to do?'
    bot.send_message(message.chat.id,text,reply_markup=generate_markup())
    
# generaye buttons
def generate_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    adding_pers = types.KeyboardButton("add person in birthday list")
    show_persons = types.KeyboardButton("show persons")
    markup.add(adding_pers, show_persons)
    return markup


# find all text messages
@bot.message_handler(content_types=['text'])

# router of coomands
def func(message):

    if(message.text == "add person in birthday list"):
        bot.send_message(message.chat.id, "Введите имя черз пробел дату:")
        bot.register_next_step_handler(message, get_name_and_day)
    if message.text == "/print":
        print_data(message)    
    if message.text=="show persons":
        print_data(message)

# funct to add new line in dictionary
def get_name_and_day(message):
    chat_id = message.chat.id
    name_and_day = message.text
    name_and_day=str(name_and_day)
    name_and_day=name_and_day.split()
    name=name_and_day[0]
    day=name_and_day[1]
    data_dict[name]=day

# print data_dict
def print_data(message):
    
    chat_id = message.chat.id
    data_text = "Содержимое словаря:\n"
    for key, value in data_dict.items():
        data_text += f"{key}: {value}\n"
    bot.send_message(chat_id, data_text)

    
bot.polling(non_stop=True)