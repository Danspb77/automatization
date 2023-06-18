import telebot
from telebot import types

# token from telegram
bot=telebot.TeleBot("6235774110:AAFhV7WQ96YjqkvbRTl5-usGzPoue9lF4rU")



@bot.message_handler(commands=['start'])

def start(message):
    text=f'hello, {message.from_user.first_name}'
    bot.send_message(message.chat.id,text ,parse_mode='html')

bot.polling(non_stop=True)