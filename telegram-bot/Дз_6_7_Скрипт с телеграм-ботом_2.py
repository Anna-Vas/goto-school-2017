import telebot, uuid, requests
from PIL import Image
from threading import Thread
from time import sleep

token = '353968427:AAHvZBHlnCCJIxE3znYquJ6T1wRTzPpbWeI'
bot = telebot.TeleBot(token)

def process(filename):
    file = open(filename, 'rb')
    image_data = file.read() 
    headers={ 
        "Content-Type": "application/octet-stream", 
      "Ocp-Apim-Subscription-Key": "ed949f112a524980ad1907524eb7d32d" 
    } 
    url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize" 
    result = requests.post(url, data=image_data, headers=headers) 
    faces_list = result.json()
    im = Image.open(filename)
    for face in faces_list:
        coords = face['faceRectangle']
        emotions = face['scores']
        emotions_list = list(emotions.items())
        faces_sorted = sorted(emotions_list, key=lambda x: x[1], reverse=True)
        
        if faces_sorted[0][0] == "happiness":
            smile = Image.open('smile.png').convert('RGBA')
        elif faces_sorted[0][0] == 'contempt':
            smile = Image.open('smile_pr.png').convert('RGBA')
        elif faces_sorted[0][0] == 'anger':
            smile = Image.open('smile_anger.png').convert('RGBA')
        elif faces_sorted[0][0] == 'disgust':
            smile = Image.open('smile_dis.png').convert('RGBA')
        elif faces_sorted[0][0] == 'disgust':
            smile = Image.open('smile_dis.png').convert('RGBA')
        elif faces_sorted[0][0] == 'fear':
            smile = Image.open('smile_fear.png').convert('RGBA')
        elif faces_sorted[0][0] == 'sadness':
            smile = Image.open('smile_sad.png').convert('RGBA')
        elif faces_sorted[0][0] == 'neutral':
            smile = Image.open('smile_neutral.png').convert('RGBA')
        elif faces_sorted[0][0] == 'surprise':
            smile = Image.open('smile_surprise.png').convert('RGBA')
        smile = smile.resize((coords['width'], coords['height']))
    
        x1 = coords['left']
        y1 = coords['top']
    
        x2 = x1 + coords['width']
        y2 = y1 + coords['height']
        box = (x1, y1, x2, y2)
        
        im.paste(smile, box, smile)

        im.save(filename)

@bot.message_handler(commands=["start"])
def start_spam(message):
    bot.send_message(message.chat.id, "Привет! Меня зовут Афина, и я могу исполнять твои команды.\nПришли мне код на языке Python, и я его исполню.\nОтправь мне фото, и я обработаю его так, что тебе точно понравится ;)\nСлабо написать мне команду /spam и посмотреть, что получится? Только осторожнее, на всякий случай запомни команду /stop\nКроме того, у меня есть секретная функция: попробуй найти ко мне подход, и тебя ждёт сюрприз!")

@bot.message_handler(content_types=["photo"])
def save(message):
    try:
        #скачивание файла
        file_id = message.photo[-1].file_id
        path = bot.get_file(file_id)
        downloaded_file = bot.download_file(path.file_path)

        #узнаешь расширение и придумываем имя
        extn = '.' + str(path.file_path).split('.')[-1]
        cname = str(uuid.uuid4()) + extn

        #создаем файл и записываем туда данные
        with open(cname, 'wb') as new_file:
            new_file.write(downloaded_file)

        #применяем фильтр
        process(cname)

        #открываем файл и отправляем его пользователю
        with open(cname, 'rb') as new_file:
            bot.send_photo(message.chat.id, new_file.read())
    except Exception as e:
        bot.send_message(message.chat.id, 'Извините, в данный момент функция обработки изображений недоступна. Попробуйте позже.')

users = []

@bot.message_handler(commands=['spam'])
def start_spam(message):
    users.append(message.chat.id)
    bot.send_message(message.chat.id, 'Мне скучно на Олимпе. Мы целыми днями пьём нектар и...')
    
@bot.message_handler(commands=["stop"])
def start_spam(message):
    users.remove(message.chat.id)
    bot.send_message(message.chat.id, "Просишь пощады? Уже совершил жертвоприношение в мою честь? Ладно, на первый раз прощу и так.")

def update_messages():
    bot.polling(none_stop=True)

def send_spam():
    while True:
        for user in users:
            bot.send_message(user, "Достаём смертных божественным спамом!")
        sleep(3)

polling = Thread(target=update_messages)
spamming = Thread(target=send_spam)

polling.start()
spamming.start()

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == 'Афина, ты самая красивая среди богинь':
        result = 'Спасибо за комплимент. Если бы Парис считал так же, не была бы развязана троянская война!'
    else:
        try:
            result = eval(message.text)
        except Exception as e:
            result = 'Афина не понимает тебя. Твой язык слишком бессмысленный для богов Олимпа, смертный. Разговаривай со мной на моём языке!'
    bot.send_message(message.chat.id, result)
