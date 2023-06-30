from .database import Database
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, Message,
                           ReplyKeyboardMarkup, KeyboardButton, CallbackQuery)
import telebot

from random import randint, choice
from threading import Thread
from time import sleep
import requests
import urllib
import re

words = ['пицца', 'ангел', 'мираж', 'носки', 'выдра', 'петух']
heartSymbol = u'\u2764'


class Bot(telebot.TeleBot):
    def __init__(self, token: str) -> None:
        super().__init__(token)

        self.database = Database('users.json')
        self.url = 'http://www.youtube.com/results?'
        self.pattern = re.compile(r'watch\?v=(\S{11})')
        self.stickers = {
            'pentagon': 'CAACAgIAAxkBAAEHoKBj4nxkZeZhnGBhn1-I2YMoxcauKAACrhQAAkOwIEtbmzCLsmAXoy4E',
            'calculator': 'CAACAgEAAxkBAAEHoJ5j4nwuhXGVUA3rL-hbogOAK4NZGAACRAIAAlGXOER2LcORTkW25y4E',
            'random-stickers': [
                'CAACAgIAAxkBAAEHoNxj4okqeUbzPnOPgXLrDUv05ktkHQACkSQAApF0aUhwTsMhNeo6xi4E',
                'CAACAgIAAxkBAAEHoNpj4okopzGJdwABRNMxv-yEtP1MmdUAAlcbAAKaMdBKh4jNhDabJfQuBA',
                'CAACAgIAAxkBAAEHoNhj4okiu-msDO_3sKY-cAt75xMZwQACfR8AAnEJ0EpQ7a2B5RjDZi4E',
                'CAACAgIAAxkBAAEHoNVj4okex7BiWDoHlCJuat6MBf2ySgACZRoAAntC0Eo6YutiV3MSei4E',
            ],
            'error': 'CAACAgIAAxkBAAEEtVlifCQm1Xk-stbixF48nKF5Zti2lAACwxMAAm3oEEqGY8B94dy6NCQE',
        }

        self.cancelMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
        self.cancelMarkup.add(KeyboardButton('❌ Отмена'))
        self.pentagonMarkup = InlineKeyboardMarkup()
        self.pentagonMarkup.add(
            InlineKeyboardButton('Начать', callback_data="pentagon-yes"),
            InlineKeyboardButton('Я передумал', callback_data="pentagon-no")
        )
        self.featuresMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        self.featuresMarkup.add(
            KeyboardButton('👮‍ Взлом пентагона'),
            KeyboardButton('🧮 Калькулятор'),
            KeyboardButton('🤯 Рандомный стикер'),
            KeyboardButton('❓ Игра "9 жизней"'),
            KeyboardButton('🎥 Искать видео'),
            KeyboardButton('🔍 Информация'),
        )

        self.register_message_handler(
            callback=self.on_start,
            commands=['start']
        )
        self.register_message_handler(
            callback=self.on_other_messages
        )

        self.register_callback_query_handler(
            callback=self.on_pentagon_call,
            func=lambda call: 'pentagon' in call.data,
        )

    def on_start(self, message: Message) -> None:
        userId = message.from_user.id

        if self.database.user_exists(userId):
            self.send_message(userId, 'Привет!')
        else:
            self.database.create_user(userId)
            self.send_message(
                userId,
                'Вас приветствует бот!',
                reply_markup=self.featuresMarkup
            )

    def on_other_messages(self, message: Message) -> None:
        userId = message.from_user.id
        userState = self.database.get_user(userId)['state']

        if userState == 'pentagon':
            self.on_pentagon_state(userId)
        elif userState == 'calculator':
            self.on_calculator_state(userId, message.text)
        elif userState == 'video':
            self.on_video_state(userId, message.text)
        elif userState == 'game-secret-word':
            self.on_game_secret_word_state(userId, message.text)
        else:
            self.on_none_state(userId, message.text, message.from_user.first_name)

    def on_pentagon_state(self, userId: int) -> None:
        self.send_message(
            userId,
            'Подождите немного, это очень трудозатратная операция!',
            reply_markup=self.featuresMarkup
        )

    def on_calculator_state(self, userId: int, text: str) -> None:
        if text == '❌ Отмена':
            markup = self.featuresMarkup
            message = 'Чем теперь займёмся?'
            self.database.update_user(userId, state='menu')

        else:
            markup = self.cancelMarkup
            try:
                resault = eval(text.replace('^', '**').replace(':', '/'))
                message = f'Ответ: {resault}.'
            except ZeroDivisionError:
                message = 'Нельзя делить на ноль!'
            except Exception:
                message = 'Введите математический пример!\nПример: (5 + 5)/2^3'

        self.send_message(userId, message, reply_markup=markup)

    def on_video_state(self, userId: int, text: str) -> None:
        if text == '❌ Отмена':
            markup = self.featuresMarkup
            message = 'Чем теперь займёмся?'
            self.database.update_user(userId, state='menu')

        else:
            message = 'Если хочешь вернуться в меню, нажми кнопку'
            markup = self.cancelMarkup
            queryString = urllib.parse.urlencode({"search_query" : text})
            result = requests.get(self.url + queryString)

            if result.ok:
                body = result.text
                links = self.pattern.findall(body)[:5]
                for link in links:
                    self.send_message(
                        userId,
                        'http://www.youtube.com/watch?v=' + link
                    )

        self.send_message(userId, text=message, reply_markup=markup)

    def on_game_secret_word_state(self, userId: int, text: str) -> None:
        if text == '❌ Отмена':
            markup = self.featuresMarkup
            message = 'Чем теперь займёмся?'
            self.database.update_user(userId, state='menu')

        else:
            text = text.lower()
            markup = self.cancelMarkup
            user = self.database.get_user(userId)
            word = list('?' * len(user['nineLivesWord']))

            for i, letter in enumerate(user['nineLivesWord'][:len(text)]):
                if user['nineLivesWord'][i] == text[i]:
                    word[i] = text[i]

            if word == user['nineLivesWord']:
                markup = self.featuresMarkup
                points = user['nineLivesHealth'] * 10
                message = f'Победа! Вы заработали {points} очков.'
                self.database.update_user(
                    userId,
                    state=None,
                    nineLivesPoints=user['nineLivesPoints'] + points
                )

            elif user['nineLivesHealth'] > 0:
                health = user['nineLivesHealth'] - 1
                message = 'Неправильно! Вы теряете одну жизнь!\n'
                message += 'Слово: ' + ' '.join(word) + '\n'
                message += 'Осталось жизней: ' + heartSymbol * health
                self.database.update_user(userId, nineLivesHealth=health)

            else:
                markup = self.featuresMarkup
                message = 'Вы проиграли('
                self.database.update_user(userId, state=None)

        self.send_message(userId, message, reply_markup=markup)

    def on_none_state(self, userId: int, text: str, name: str) -> None:
        if text == '👮‍ Взлом пентагона':
            self.database.update_user(userId, state='pentagon')
            self.send_sticker(userId, self.stickers['pentagon'])
            self.send_message(
                userId,
                'Вы уверены в свём решении?',
                reply_markup=self.pentagonMarkup
            )

        elif text == '🧮 Калькулятор':
            self.database.update_user(userId, state='calculator')
            self.send_message(
                userId,
                'Хорошо, теперь напишите какой-нибудь пример.',
                reply_markup=self.cancelMarkup
            )
            self.send_sticker(userId, self.stickers['calculator'])

        elif text == '🤯 Рандомный стикер':
            self.send_sticker(userId, choice(self.stickers['random-stickers']))

        elif text == '🎥 Искать видео':
            self.database.update_user(userId, state='video')
            self.send_message(
                userId,
                'Введите поисковый запрос.',
                reply_markup=self.cancelMarkup
            )

        elif text == '❓ Игра "9 жизней"':
            word = choice(words)
            print(word)
            self.database.update_user(
                userId,
                state='game-secret-word',
                nineLivesWord=list(word),
                nineLivesHealth=9
            )
            message = 'Это игра 9 жизней, попробуй угадать слово!\n'
            message += 'Слово: ' + '? ' * len(word) + '\n'
            message += 'Жизней: ' + heartSymbol * 9
            self.send_message(
                userId,
                message,
                reply_markup=self.cancelMarkup
            )

        elif text == '🔍 Информация':
            user = self.database.get_user(userId)
            text = f'id: {userId}\n'
            text += f'Имя: {name}\n'
            text += 'Очков в игре "9 жизней": ' + str(user['nineLivesPoints'])
            self.send_message(userId, text, reply_markup=self.featuresMarkup)

        else:
            self.send_message(
                userId,
                'Я не знаю такого действия!',
                reply_markup=self.featuresMarkup
            )
            self.send_sticker(userId, self.stickers['error'])

    def on_pentagon_call(self, call: CallbackQuery) -> None:
        if call.data == 'pentagon-yes':
            self.answer_callback_query(call.id, 'Вы сами подписались на это...')
            self.edit_message('👮 Взлом пентагона... 0%', call)
            Thread(target=self.on_hacking, args=(call,)).start()

        else:
            self.database.update_user(call.from_user.id, state=None)
            self.answer_callback_query(call.id, 'Вот и славненько')
            self.edit_message('Отменено.', call)

    def on_hacking(self, call: CallbackQuery) -> None:
        percent = 1
        while percent < 100:
            sleep(randint(5, 7) / 10)
            self.edit_message(f'👮 Взлом пентагона... {percent}%', call)
            percent += randint(2, 5)

        self.edit_message('👮 Взлом пентагона... 100%', call)
        sleep(2)
        if randint(0, 1):
            self.edit_message('🟢 Пентагон успешно взломан!', call)
        else:
            self.edit_message('🦠 Вы подхватили вирус на Ваше устройство!', call)
        self.database.update_user(call.from_user.id, state='menu')

    def edit_message(
        self,
        text: str,
        call: CallbackQuery,
        markup = InlineKeyboardMarkup()
    ) -> None:
            try:
                self.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup
                )
            except Exception:
                pass
