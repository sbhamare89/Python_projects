import telebot
import download


bot = telebot.TeleBot("1085683373:AAGxqXQrIpdPbPYzn9lgYg8GSubIttpESOM")

@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey! how are you ?")

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "hello")

@bot.message_handler(commands='update')
def update(message):
    download.NseIndia()

@bot.message_handler(commands=['chart'])
def latest(message):
    bot.send_message(message.chat.id, "charts")

bot.polling()