import telebot
from Extensions import CryptoConverter, ConvertionException
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n <имя валюты> \
<в какую валюту перевести>\
<количество переводимой валюты>\nУвидеть список всех доступных валют: /<values>'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if(len(values)) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        amount_float = float(amount)
        total_base = CryptoConverter.convert(quote, base, amount)
        convertion_result = round((amount_float * total_base), 2)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользоваеля.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Курс {base} к {quote} - {total_base}\nЦена {amount} {quote} в {base} - {convertion_result}.'
        bot.send_message(message.chat.id, text)

bot.polling()

