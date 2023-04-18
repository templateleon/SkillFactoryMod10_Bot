import traceback
import telebot
from telebot import types
from config import keys, TOKEN
from utils import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

error_text = 'Введите валюты заново или выберите Меню --> Кнопки'


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    text = 'Привет! \nЭто бот Меняла он поможет рассчитать \nсумму средств при обмене валют. \nДля получения справки или списка \nдоступных валют войдите в меню'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту через пробел в следующем формате: \n1) Название валюты которую собираетесь потратить. \n2) Название валюты которую собираетесь купитью  \n3) Количество покупаемой валюты. \nНапример: евро рубль 100 \n\n**Или выберите Меню --> Кнопки**'
    bot.send_message(message.chat.id, text)


def btn_generator():
    btn = []
    button = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn.extend(types.KeyboardButton(text=key.upper()) for key in keys.keys())
    # btn = [(types.KeyboardButton(text=key.upper())) for key in keys.keys()]
    button.add(*btn)
    return button


@bot.message_handler(commands=['values', 'key'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты'
    if message.text == '/values':
        for key in keys.keys():
            text = '\n'.join((text, key))
        bot.reply_to(message, text)
    if message.text == '/key':
        text = 'Что будем тратить?'
        bot.send_message(message.chat.id, text, reply_markup=btn_generator())
        bot.register_next_step_handler(message, buy)


def buy(message: telebot.types.Message):
    quote = message.text
    text = 'Что покупаем?'
    bot.send_message(message.chat.id, text, reply_markup=btn_generator())
    bot.register_next_step_handler(message, sell, quote)


def sell(message: telebot.types.Message, quote):
    base = message.text
    text = 'Сколько будем покупать?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, spend, quote, base)


def spend(message: telebot.types.Message, quote, base):
    amount = message.text
    values = quote, base, amount
    try:
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')
        purchase_amount = CurrencyConverter.convert(*values)
    except ConvertionException as exc:
        bot.reply_to(message, f"Ошибка:\n{exc}")
    except Exception as exc:
        traceback.print_tb(exc.__traceback__)
        bot.reply_to(message, f"Ошибка соединения:\n{exc} \n{error_text}")
    else:
        bot.reply_to(message, purchase_amount)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise ConvertionException(
                f'Неверное количество параметров. {error_text}')
        purchase_amount = CurrencyConverter.convert(*values)
    except ConvertionException as exc:
        bot.reply_to(message, f"Ошибка:\n{exc}")
    except Exception as exc:
        traceback.print_tb(exc.__traceback__)
        bot.reply_to(message, f"Ошибка:\n{exc}  {error_text}")
    else:
        bot.reply_to(message, purchase_amount)


bot.polling(none_stop=True)
