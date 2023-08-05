import telebot
from telebot import types
import json
from datetime import datetime

# token from telegram
bot=telebot.TeleBot("6235774110:AAFhV7WQ96YjqkvbRTl5-usGzPoue9lF4rU")

# dictionary to load into databse
data_dict = {
        "dan":2746,
        "mom":845
    }
with open("data.json", "r") as read_file:
    data_dict = json.load(read_file)


today=datetime.today()
today=today.strftime("%d/%m/%Y")

# calculate age
def age_calculation(value):
    date_string = str(value)
    date_object = datetime.strptime(date_string, "%d/%m/%Y")
    date_object=date_object.year
    now = datetime.now()
    now=now.year

    delta = now - date_object

    return( delta)




@bot.message_handler(commands=['welcome'])

def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Start", callback_data="start")
    markup.add(start_button)
    
    user_name = message.from_user.first_name
    text=f'hello, {user_name}, I\'m bot which will remind\
     you about birhdays'
    bot.send_message(message.chat.id,text ,parse_mode='html')

    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы начать:", reply_markup=markup)

            
# congreeting messages
@bot.message_handler(commands=['start'])

def start(message):
    # generate_start_buttom(message)
    
    

    text='What would you like to do?'
    bot.send_message(message.chat.id,text,reply_markup=generate_markup())
    birthday_check(message)


@bot.callback_query_handler(func=lambda call: call.data == "start")
def process_callback_start(call):
   
    start(call.message)        
    
    
# generate buttons
def generate_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    adding_pers = types.KeyboardButton("add person in birthday list")
    show_persons = types.KeyboardButton("show persons")
    birth_today=types.KeyboardButton("imenninik")
    birth_during_week=types.KeyboardButton("blizko")
    delete_person=types.KeyboardButton("delete_person")
    markup.add(adding_pers, show_persons,birth_today,birth_during_week,delete_person)
    return markup


# find all text messages
@bot.message_handler(content_types=['text'])

# router of coomands
def func(message):

    if(message.text == "add person in birthday list"):
        bot.send_message(message.chat.id, "Введите имя черз пробел дату день/месяц/год:")
        bot.register_next_step_handler(message, get_name_and_day)
        
    if message.text=="show persons":
        print_data(message)
    if message.text=="imenninik":
        birthday_check(message)
    if message.text=="blizko":
        week_check(message)
    if message.text=="delete_person":
        bot.send_message(message.chat.id, "Введите имя of deleting person:")
        bot.register_next_step_handler(message, delete_person)
        
        

# funct to add new line in dictionary
def get_name_and_day(message):
    chat_id = message.chat.id
    name_and_day = message.text
    name_and_day=str(name_and_day)
    name_and_day=name_and_day.split()
    name=name_and_day[0]
    day=name_and_day[1]
    data_dict[name]=day
    with open('data.json', 'w') as outfile:
        json.dump(data_dict, outfile)
    bot.send_message(message.chat.id, "Данные успешно записаны")

# print data_dict
def print_data(message):
    with open("data.json", "r") as read_file:
        data_dict = json.load(read_file)

    chat_id = message.chat.id
    data_text = "Содержимое списка:\n"
    for key, value in data_dict.items():
        data_text += f"{key}: {value}\n"
    bot.send_message(chat_id, data_text)

def delete_person(message):
    person=message.text
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Удаляем ключ
    if person in data:
        del data[person]

    # Записываем обновленный JSON обратно в файл
    with open('data.json', 'w') as f:
        json.dump(data, f)    
        
    
        bot.send_message(message.chat.id, "Данные успешно удалены")


# check if anyone has birthday today
def birthday_check(message):
        for key, value in data_dict.items():
            if today[:5] in value:

                print(f"{key}: {value}")
                age=age_calculation(value)

                # checking anniversary ubiley
                if age % 5==0:
                    text= f"сегодня <b>юбилей</b> рождения у {key}: {value}, ему исполнилось {age} "
                    bot.send_message(message.chat.id,text ,parse_mode='html')
                else:
                    text= f"сегодня день рождения у {key}: {value}, ему {age} "
                    bot.send_message(message.chat.id,text ,parse_mode='html')


def plus_week(value):

    value=value[:5]
    date_object=datetime.strptime(value + "/" + str(datetime.now().year), "%d/%m/%Y")
    now=datetime.now()
    differnce=date_object-now
    differnce=differnce.days
    if 0<=differnce<=7:
        return True
    else:
        return False

# check if anyone has birthday during the week
def week_check(message):
    for key, value in data_dict.items():
        if plus_week(value)==True:
            age=age_calculation(value)
            text= f"меньше чем через неделю будет день рождения у {key}: {value}, ему {age} "
            bot.send_message(message.chat.id,text ,parse_mode='html')

    
bot.polling(non_stop=True)