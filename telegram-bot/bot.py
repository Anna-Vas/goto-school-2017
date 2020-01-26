import telebot, uuid, requests
from PIL import Image
from threading import Thread
from time import sleep

token = '1337'  # Replace 1337 with your telegram bot token
bot = telebot.TeleBot(token)

# Image processing function
def process(filename):
    # Opening and reding image
    file = open(filename, 'rb')
    image_data = file.read() 
    headers={ 
        "Content-Type": "application/octet-stream", 
      "Ocp-Apim-Subscription-Key": "ed949f112a524980ad1907524eb7d32d" 
    }
    # Query to Microsoft Azure server for emotions recognition
    url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize" 
    result = requests.post(url, data=image_data, headers=headers)
    faces_list = result.json()
    # Getting all faces from the image
    im = Image.open(filename)
    for face in faces_list:
        coords = face['faceRectangle']
        emotions = face['scores']
        emotions_list = list(emotions.items())
        faces_sorted = sorted(emotions_list, key=lambda x: x[1], reverse=True)
        # Finding matching emoji for every face
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
        # Resizing emojis so they would fit the faces
        smile = smile.resize((coords['width'], coords['height']))
    
        # Replacing faces with emojis
        x1 = coords['left']
        y1 = coords['top']
    
        x2 = x1 + coords['width']
        y2 = y1 + coords['height']
        box = (x1, y1, x2, y2)
        
        im.paste(smile, box, smile)

        # Saving result
        im.save(filename)

# Greeting message
@bot.message_handler(commands=["start"])
def start_spam(message):
    bot.send_message(message.chat.id, "Hey! My name is Athena. I can respond your commands.\nSend me some Python code and I will execute it.\nSend me a photo and I'll send you back something you will defenitely like.\nI dare you to send me a command /spam and see what happens (be careful and remember another command /stop).\nBesides, I have a secret function: find an approach to me and you'll be surprised!!")

@bot.message_handler(content_types=["photo"])
def save(message):
    try:
        # Downloading a file
        file_id = message.photo[-1].file_id
        path = bot.get_file(file_id)
        downloaded_file = bot.download_file(path.file_path)

        # Getting file extension
        extn = '.' + str(path.file_path).split('.')[-1]
        cname = str(uuid.uuid4()) + extn

        # Creating a file and writing there downloaded image
        with open(cname, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Applying filter
        process(cname)

        # Sending result to user
        with open(cname, 'rb') as new_file:
            bot.send_photo(message.chat.id, new_file.read())

    # Error message in case Microsoft Azure server is not responding
    except Exception as e:
        bot.send_message(message.chat.id, 'Sorry, image processing function is unavailable right now. Try again later.')

users = []

# Message before starting spam
@bot.message_handler(commands=['spam'])
def start_spam(message):
    users.append(message.chat.id)
    bot.send_message(message.chat.id, 'I get bored on Olympus. We drink nectar the whole day and...')

# Message after stopping spam
@bot.message_handler(commands=["stop"])
def start_spam(message):
    users.remove(message.chat.id)
    bot.send_message(message.chat.id, "Are you asking for mercy? Already made a sacrifice in my honor? Okay, for the first time I forgive you anyway.")

# Continiously updating for new incoming messages
def update_messages():
    bot.polling(none_stop=True)

# Continiously sending spam every three seconds to users who are in the spam list
def send_spam():
    while True:
        for user in users:
            bot.send_message(user, "Irritate mortals with godlike spam!")
        sleep(3)

# Multithreading for executing two endless cycles at the same time
polling = Thread(target=update_messages)  # updating for new messages
spamming = Thread(target=send_spam)  # sending spam

polling.start()
spamming.start()

# Text messages processing
@bot.message_handler(content_types=["text"])
def answer(message):
    # Secret function
    if message.text == 'Athena, you are the most beautiful goddess!':
        result = "Thank you for the compliment. If Paris thought the same, the Trojan was wouldn't have been unleashed!"
    # Python code executing
    else:
        try:
            result = eval(message.text)
        # Common answer for all other messages
        except Exception as e:
            result = 'Athena does not understand you. Your language is too meaningless for the gods of Olympus, mortal. Talk to me in my language!'
    # Sending message
    bot.send_message(message.chat.id, result)
