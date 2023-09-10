import telebot
from telebot import types
import json
from datetime import datetime
import re

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




# @bot.message_handler(commands=['start'])

# def send_welcome(message):
#     markup = types.InlineKeyboardMarkup()
#     start_button = types.InlineKeyboardButton(text="Start \U0001F4AB", callback_data="start")
#     markup.add(start_button)
    
#     # user_name = message.from_user.first_name
#     # text=f'Привет, {user_name}  \U0001F44B я бот, который будет напоминать тебе о днях рождения \U0001F603'
       
#     # bot.send_message(message.chat.id,text ,parse_mode='html')

#     bot.send_message(message.chat.id, "Нажми на кнопку, чтобы начать:", reply_markup=markup)

            
# congreeting messages
@bot.message_handler(commands=['start'])

def send_welcome(message):
    user_name = message.from_user.first_name
    text=f'Привет, {user_name}  \U0001F44B я бот, который будет напоминать тебе о днях рождения \U0001F603'
        
    bot.send_message(message.chat.id,text ,parse_mode='html')
    start(message)


def start(message):
    
    text='Что вы хотите сделать?'
    bot.send_message(message.chat.id,text,reply_markup=generate_markup())
    


@bot.callback_query_handler(func=lambda call: call.data == "start")
def process_callback_start(call):
   
    start(call.message)        
    
    
# generate buttons
def generate_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    adding_pers = types.KeyboardButton("добавить человека в список \U0001F4D1")
    show_persons = types.KeyboardButton("показать список \U0001F466")
    birth_today=types.KeyboardButton("день рождения сегодня \U0001F389")
    birth_during_week=types.KeyboardButton("дни рождения в ближайшую неделю \U0001F4C6")
    delete_person=types.KeyboardButton("удалить человека из списка \U0000274C")
    markup.add(adding_pers, show_persons,birth_today,birth_during_week,delete_person)
    return markup


# find all text messages
@bot.message_handler(content_types=['text'])

# router of coomands 
def func(message):

    if(message.text == "добавить человека в список \U0001F4D1"):
        bot.send_message(message.chat.id, "Введите имя через пробел дату день/месяц/год:")
        bot.register_next_step_handler(message, get_name_and_day)
        
    if message.text==f"показать список \U0001F466":
        print_data(message)
    if message.text==f"день рождения сегодня \U0001F389":
        birthday_check(message)
    if message.text=="дни рождения в ближайшую неделю \U0001F4C6":
        week_check(message)
    if message.text=="удалить человека из списка \U0000274C":
        bot.send_message(message.chat.id, "Введите имя человека, которого хотите удалить :")
        bot.register_next_step_handler(message, delete_person)
        
        
# check format of date string
def format_check(day):
    patt=r'(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)'
    if  re.match(patt,day)!=None:
        return True
    return False

#  funct to check surname exist ?
def surname_check(name):
    name_and_surname=''
    for i in range(len(name)):
        name_and_surname=name[i]+' '+ name_and_surname
    return name_and_surname.rstrip()


# funct to add new line in dictionary
def get_name_and_day(message):
    
    name_and_day = message.text
    name_and_day=str(name_and_day)
    name_and_day=name_and_day.split()

    name=name_and_day[0:len(name_and_day)-1]
    day=name_and_day[len(name_and_day)-1]
    data_dict[surname_check(name)]=day
    if format_check(day)==True:
        with open('data.json', 'w') as outfile:
            json.dump(data_dict, outfile)
        bot.send_message(message.chat.id, "Данные успешно записаны  \U00002705")
        start(message)
    else:
        bot.send_message(message.chat.id, "Не удалось записать данные,попробуйте другой формат ввода  \U0001F501")
            
        start(message)

# format data for printing
def format_printing_data(value):
    value=str(value)
    value=value.replace('/','.')
    return value

# print data_dict
def print_data(message):
    with open("data.json", "r") as read_file:
        data_dict = json.load(read_file)
    if len(data_dict)>0:
        chat_id = message.chat.id
        data_text = "Содержимое списка:\n"
        for key, value in data_dict.items():
            data_text += f"{key} - {format_printing_data(value)}\n"
        bot.send_message(chat_id, data_text)
        start(message)
    else:
        chat_id = message.chat.id
        data_text = "список пуст"
        bot.send_message(chat_id, data_text)
        start(message)

# deletepersons
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
        start(message)
    else:
        bot.send_message(message.chat.id, "такого человека нет в списке, повторите попытку \U0001F501")
        start(message)


# check if anyone has birthday today
def birthday_check(message):
        with open("data.json", "r") as read_file:
            data_dict = json.load(read_file)
        flag=False
        counter=len(data_dict)
        print(counter)
        for key, value in data_dict.items():
            if today[:5] in value:

                
                age=age_calculation(value)

                # checking anniversary ubiley
                if age % 5==0:
                    text= f"сегодня <b>юбилей</b>  у {key}: {value}, ему исполнилось {age} "
                    bot.send_message(message.chat.id,text ,parse_mode='html')
                    flag=True
                else:
                    text= f"сегодня день рождения у {key}: {value}, ему {age} "
                    bot.send_message(message.chat.id,text ,parse_mode='html')
                    flag=True
        if flag==False:
            text=f"сегодня ни у кого нет дня рождения"
            bot.send_message(message.chat.id,text, parse_mode='html')


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
    flag=False
    for key, value in data_dict.items():
        if plus_week(value)==True:
            flag=True
            age=age_calculation(value)
            text= f"меньше чем через неделю будет день рождения у {key}: {value}, ему {age} "
            bot.send_message(message.chat.id,text ,parse_mode='html')
            
    if flag==True:
        start(message)

    if flag==False:
        text= f"ни у кого нет дня рождения в ближайшие 7 дней "
        bot.send_message(message.chat.id,text ,parse_mode='html')
        start(message)

bot.polling(non_stop=True)