import telebot, uuid, requests
from PIL import Image

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

@bot.message_handler(content_types=["photo"])
def save(message):
    try:
        file_id = message.photo[-1].file_id
        path = bot.get_file(file_id)
        downloaded_file = bot.download_file(path.file_path)

        extn = '.' + str(path.file_path).split('.')[-1]
        cname = str(uuid.uuid4()) + extn

        with open(cname, 'wb') as new_file:
            new_file.write(downloaded_file)

        process(cname)

        with open(cname, 'rb') as new_file:
            bot.send_photo(message.chat.id, new_file.read())
    except Exception as e:
        bot.send_message(message.chat.id, 'Sorry, this feature is unavailable right now. Try later.')

bot.polling(none_stop=True)
