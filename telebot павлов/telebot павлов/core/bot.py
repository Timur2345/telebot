import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from .database import Database

class Bot(telebot.TeleBot):
    def __init__(self,token):
        super().__init__(token)
        self.database = Database('user.json')
        self.featuresMarkup=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        self.featuresMarkup.add(
            KeyboardButton('🤗взлом пентагона'),
            KeyboardButton('Калькулятор'),
            KeyboardButton('💖9 жизней'),
            KeyboardButton('😮Поиск видео'),
            KeyboardButton('🎬Рандомный стикер'),
            KeyboardButton('😶❓Информация')
        )
        self.register_message_handler(callback=self.on_start,commands=['start'])

        self.register_message_handler(callback=self.on_other_message)
    
    def on_start(self,message):
        userId = message.from_user.id

        if self.database.user_exists(userId):
            name=message.from_user.full_name
            self.send_message(userId,'Привет!'+name)
        else:
            self.database.create_user(userId)
            self.send_message(
                userId,
                'Вас приветствует бот!',
                reply_markup=self.featuresMarkup
            )
    def on_other_message(self,message):
        passuserId = message.from_user.id
        userState = self.database.get_user(userId)['state']
        self.on_none_state(userId, message.text, message.from_user.first_name)
    def on_none_state(self,userId,text,name):
        if text == '🤗взлом пентагона':
            pass
        elif text ==  'Калькулятор':
            pass
        elif text ==  '💖9 жизней':
            pass
        elif text ==  '😮Поиск видео':
            pass
        elif text ==  '🎬Рандомный стикер':
            pass
        elif text ==  '😶❓Информация':
            pass
        else:
            self.send_message(userId, 'я не знаю такой команды!', reply_markup=self.featuresMarkup)