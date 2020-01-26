from PIL import Image
import requests

# Generate new file name
def new_file_name(oldname, filtername):
    list_file_name = oldname.split('.')
    return list_file_name[0] + '_' + filtername + '.' + list_file_name[1]

# Get image for processing
imagename = input('File to process (with path): ')

filter_ = 0

# User chooses filter
while filter_ != 'q':
    filter_ = input('Choose filter:\nv for violet sunset\ns for stripes\nf for fire\ng for gradient\np for poster\nh for replacing faces with emojis;\nq to exit: ')

    # Apply violet sunset filter
    if filter_ == 'v':
        # Open and read image
        image = Image.open(imagename)
        pixels = image.load()
        # Edit pixels
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
        # Save result
        output_file_name = new_file_name(imagename, 'violet')
        image.save(output_file_name)
        image.show()

    # Apply stripes filter
    elif filter_ == 's':
            # Open and read image
            image = Image.open(imagename)
            pixels = image.load()
            # Define size of one stripe
            h = image.height // 10
            h0 = 0
            hn = h
            k = 20
            f = 0
            # Create stripes
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
            # Save result
            output_file_name = new_file_name(imagename, 'stripes')
            image.save(output_file_name)
            image.show()

    # Apply fire filter
    elif filter_ == 'f':
        # Open and read image
        image = Image.open(imagename)
        pixels = image.load()
        # Edit pixels
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
        # Save result
        output_file_name = new_file_name(imagename, 'fire')
        image.save(output_file_name)
        image.show()

    # Apply gradient filter
    elif filter_ == 'g':
        # Open and read file
        image = Image.open(imagename)
        pixels = image.load()
        # Define size of one area
        h = image.height // 100
        h0 = 0
        hn = h
        k = 0
        f = 0
        # Change brightness of every area
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
        # Save result
        output_file_name = new_file_name(imagename, 'gradient')
        image.save(output_file_name)
        image.show()

    # Apply poster filter
    elif filter_ == 'p':
        # Open and read image
        image = Image.open(imagename)
        pixels = image.load()
        # Edit pixels
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                S = r + g + b
                # All bright pixels become white
                if (S > (((255 - 100) // 2) * 3)):
                    r, g, b = 255, 255, 255
                # All dark pixels become green
                else:
                    r, g, b = 30, 100, 0
                pixels[i, j] = (r, g, b)
        # Save result
        output_file_name = new_file_name(imagename, 'poster')
        image.save(output_file_name)
        image.show()

    # Replace faces with emojis
    elif filter_ == 'h':
        # Open and read image
        file = open(imagename, 'rb')
        image_data = file.read() 
        headers={ 
           "Content-Type": "application/octet-stream", 
          "Ocp-Apim-Subscription-Key": "ed949f112a524980ad1907524eb7d32d" 
        }
        # Request to Microsoft Azure service for emotions recognition
        url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize" 
        result = requests.post(url, data=image_data, headers=headers)
        # Get result
        faces_list = result.json()
        im = Image.open(imagename)
        # Define coords and emotions of every face on the image
        for face in faces_list:
            coords = face['faceRectangle']
            emotions = face['scores']
            emotions_list = list(emotions.items())
            faces_sorted = sorted(emotions_list, key=lambda x: x[1], reverse=True)
            # Find matching emoji for every face
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

            # Resize every emoji for every face
            smile = smile.resize((coords['width'], coords['height']))

            # Replace faces with emojis
            x1 = coords['left']
            y1 = coords['top']
    
            x2 = x1 + coords['width']
            y2 = y1 + coords['height']
            box = (x1, y1, x2, y2)
        
            im.paste(smile, box, smile)

        # Save result
        output_file_name = new_file_name(imagename, 'smile')
        im.save(output_file_name)
        im.show()

    # Exit
    elif filter_ == 'q':
        print('Goodbuy!')

    # Wrong input handling
    else:
        print('Wrong symbol.')
