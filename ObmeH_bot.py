import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду через пробел в следующем формате:\n<имя валюты> \
<в какую перевести> \
< количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = value
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'(читать с каким-нибудь акцентом)\n {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()


