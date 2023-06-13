import telebot 
mybot = telebot.TeleBot('5963564841:AAF1HMsgUWQ-NTXxW1aFAd-gk6Jm8sn9epM') 
from telebot import types 
@mybot.message_handler(commands=['start']) 
def startBot(message): 
    first_mess=f'<b>{message.from_user.first_name}</b>, привет! \n Хочешь расскажу об Макдональдсе!'
    markup = types.InlineKeyboardMarkup()
    button_yes =types.InlineKeyboardButton(text = 'Да',callback_data='yes')
    markup.add(button_yes)
    mybot.send_message(message.chat.id, first_mess, parse_mode='html',reply_markup=markup)
@mybot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:
        if function_call.data == 'yes':
            second_mess='Мы не знаем ничего об этой компании,знаем только вкусно и точка'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text = 'сам ищи',url='https://ru.wikipedia.org/'))
            mybot.send_message(function_call.message.chat.id,second_mess,reply_markup=markup)
            mybot.answer_callback_query(function_call.id)
mybot.infinity_polling()