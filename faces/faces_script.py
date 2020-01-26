from PIL import Image
import requests

def new_file_name(oldname, filtername):
    list_file_name = oldname.split('.')
    return list_file_name[0] + '_' + filtername + '.' + list_file_name[1]

imagename = input('Введите имя изображения, которое вы хотите изменить: ')

filter_ = 0

while filter_ != 'q':
    filter_ = input('Выберите фильтр.\nЕсли вы хотите использовать фильтр "Фиолетовый закат", нажмите v;\nесли хотите использовать фильтр "Полосы", нажите s;\nесли хотите использовать фильтр "Зарево", нажмите f;\nесли хотите использовать фильтр "Градиент", нажмите g;\nесли хотите использовать фильтр "Постер", нажмите p;\nесли хотите использовать наложение смайликов, нажмите h;\nесли хотите выйти из программы, нажмите q: ')
    if filter_ == 'v':
        image = Image.open(imagename)
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                middle = (r + g + b) // 3
                r = middle + 2
                g = middle
                b = middle
                r = min(r + 100, 255)
                b = min(b + 100, 255)
                g = max(g - 100, 0)
                pixels[i, j] = (r, g, b)
        output_file_name = new_file_name(imagename, 'violet')
        image.save(output_file_name)
        image.show()
    elif filter_ == 's':
            image = Image.open(imagename)
            pixels = image.load()
            h = image.height // 10
            h0 = 0
            hn = h
            k = 20
            f = 0
            while f < image.height:
                for j in range(h0, hn):
                    for i in range(image.width):
                        r, g, b = pixels[i, j]
                        r = min(r + 120 - k, 255)
                        b = min(b + 120 - k, 255)
                        g = min(g + 120 - k, 255)
                        pixels[i, j] = (r, g, b)
                f = hn
                h0 = hn
                hn = min(hn + h, image.height)
                k += 20
            output_file_name = new_file_name(imagename, 'stripes')
            image.save(output_file_name)
            image.show()
    elif filter_ == 'f':
        image = Image.open(imagename)
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                middle = (r + g + b) // 3
                r = middle + 2
                g = middle
                b = middle
                r = min(r + 100, 255)
                b = max(b - 100, 0)
                pixels[i, j] = (r, g, b)
        output_file_name = new_file_name(imagename, 'fire')
        image.save(output_file_name)
        image.show()
    elif filter_ == 'g':
        image = Image.open(imagename)
        pixels = image.load()
        h = image.height // 100
        h0 = 0
        hn = h
        k = 0
        f = 0
        while f < image.height:
            for j in range(h0, hn):
                for i in range(image.width):
                    r, g, b = pixels[i, j]
                    r = min(r + 200 - k, 255)
                    b = min(b + 200 - k, 255)
                    g = min(g + 200 - k, 255)
                    pixels[i, j] = (r, g, b)
            f = hn
            h0 = hn
            hn = min(hn + h, image.height)
            k += 4
        output_file_name = new_file_name(imagename, 'gradient')
        image.save(output_file_name)
        image.show()
    elif filter_ == 'p':
        image = Image.open(imagename)
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                S = r + g + b
                if (S > (((255 - 100) // 2) * 3)):
                    r, g, b = 255, 255, 255
                else:
                    r, g, b = 30, 100, 0
                pixels[i, j] = (r, g, b)
        output_file_name = new_file_name(imagename, 'poster')
        image.save(output_file_name)
        image.show()
    
    elif filter_ == 'h':
        file = open(imagename, 'rb')
        image_data = file.read() 
        headers={ 
           "Content-Type": "application/octet-stream", 
          "Ocp-Apim-Subscription-Key": "ed949f112a524980ad1907524eb7d32d" 
        } 
        url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize" 
        result = requests.post(url, data=image_data, headers=headers) 
        faces_list = result.json()
        im = Image.open(imagename)
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
    
        output_file_name = new_file_name(imagename, 'smile')
        im.save(output_file_name)
        im.show()
            
    elif filter_ == 'q':
        print('Работа с программой окончена. До свидания.')
        
    else:
        print('Вы ввели неправильный символ')
