import telebot

from TicTacToe import *
import config

bot = telebot.TeleBot(config.token)


def num2symb(num):
    return {
        0: '.',
        1: 'x',
        2: 'o',
    }[num]


def generate_keyboard():
    pole = game.engine
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(num2symb(pole[0, 0].value), callback_data='0 0'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[0, 1].value), callback_data='0 1'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[0, 2].value), callback_data='0 2'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[1, 0].value), callback_data='1 0'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[1, 1].value), callback_data='1 1'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[1, 2].value), callback_data='1 2'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[2, 0].value), callback_data='2 0'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[2, 1].value), callback_data='2 1'),
                 telebot.types.InlineKeyboardButton(num2symb(pole[2, 2].value), callback_data='2 2'), row_width=3)
    return keyboard


game = Game()


@bot.message_handler(commands=['start'])
def start_game(message):
    game.start()
    bot.send_message(message.chat.id, '  Tic-Tac-Toe  ', reply_markup=generate_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    i, j = map(int, query.data.split())
    game.human_turn(i, j)
    game.computer_turn()
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id,
                          text='  Tic-Tac-Toe  ', reply_markup=generate_keyboard())
    if not game.engine:
        bot.send_message(query.message.chat.id, game.get_result())


bot.polling(none_stop=True, interval=0)
