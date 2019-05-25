import telebot
from subprocess import call
from threading import Thread
from time import sleep

token = '353968427:AAHvZBHlnCCJIxE3znYquJ6T1wRTzPpbWeI'

bot = telebot.TeleBot(token)

users = set()

@bot.message_handler(commands=['spam'])
def start_spam(message):
    users.add(message.chat.id)
    bot.send_message(message.chat.id, "I'm bored on Olympus. We drink nectar all day and ...")
    
@bot.message_handler(commands=["stop"])
def start_spam(message):
    users.remove(message.chat.id)
    bot.send_message(message.chat.id, "Are you asking for mercy? Already made a sacrifice in my honor? Okay, for the first time I forgive you.")


@bot.message_handler(content_types=["text"])
def messages(message):
    if message.text == 'Athena, you are the most beautiful goddess':
        result = 'Thanks for the compliment. If Paris considered the same, the Trojan War would not have started!'
    else:
        result = "Athena doesn't understand you. Your language is too meaningless for the goddess!"
    bot.send_message(message.chat.id, result)

def save(message):
    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)
    downloaded_file = bot.download_file(path.file_path)

    extn 

@bot.message_handler(content_types=["photo"])
def photofilter(message):
    

def update_messages():
    bot.polling(none_stop=True)

def send_spam():
    while True:
        for user in users:
            bot.send_message(user, "Irritate the mortals with the divine spam!")
        sleep(3)

polling = Thread(target=update_messages)
spamming = Thread(target=send_spam)

polling.start()
spamming.start()
