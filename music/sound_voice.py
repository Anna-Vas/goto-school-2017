import struct, pyaudio, wave

def new_file_name(oldname, filtername):
    list_file_name = oldname.split('.')
    return list_file_name[0] + '_' + filtername + '.' + list_file_name[1]

FORMAT = pyaudio.paInt16  # глубина звука = 16 бит = 2 байта
CHANNELS = 1  # моно
RATE = 48000  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 4000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
RECORD_SECONDS = 10  # длительность записи
RECORD_LEN = 5

audio = pyaudio.PyAudio()

# открываем поток для чтения данных с устройства записи по умолчанию
# и задаем параметры
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# открываем поток для записи на устройство вывода - динамик - с такими же параметрами
out_stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)
flag = True
number = 1

while flag:
    print('say anything to start recording')

    rec_new = -1
    frames = []
    
    for i in range(RECORD_SECONDS):
        s = 0  # сумма отсчетов за секунду
    
        # для каждого "запроса"
        for j in range(RATE // CHUNK):  # RATE//CHUNK - количество "запросов" к микрофону в секунду
    
            data = stream.read(CHUNK)  # читаем строку из байт длиной CHUNK * FORMAT = 4000*2 байт
            current_frames = struct.unpack("<" + str(CHUNK) + "h",
                                           data)  # строка -> список из CHUNK отсчетов, h - это short int
    
            # суммируем модули отсчетов - они могут быть отрицптельными
            if rec_new < 0:
                for frame in current_frames:
                    s += abs(frame)
                
            if s // RATE >= 700:
                if rec_new < 0:
                    
                    print('recording...')
                    rec_new = i
                    rec_end = min(i + RECORD_LEN, RECORD_SECONDS)
                else:
                    if i < rec_end: 
                        
                        frames += current_frames  # добавляем прочитанные отсчеты в общий список
            else:
                if rec_new >= 0 and i < rec_end:
                    
                    frames += current_frames  # добавляем прочитанные отсчеты в общий список
     
    if rec_new < 0:
        print("Not recorded")
        
    else:    
        print("finished recording")
    
            
        # удаляем каждый 4ый отсчет - увеличиваем частоту на 25%
        newframes = []
        for i in range(0, len(frames)):
            if i % 4 != 0:
                newframes.append(frames[i])
        n = len(newframes)
        newframes = newframes[::-1]
    
        musicname = input('Введите название музыкального файла, на который вы хотите наложить свой голос: ')
    
    
        music = wave.open(musicname)
        params = music.getparams()
        m = music.getnframes()
        data = music.readframes(m)
        musicframes = struct.unpack('<{0}h'.format(m), data)
    
        music_voice = []
        for i in range(0, n):
            music_voice.append((newframes[i] + musicframes[i]) // 2)
        full_wave = struct.pack('<{0}h'.format(n), *music_voice)  # список отсчетов -> строка из байт
    
        out_stream.write(full_wave)  # отправляем на динамик
    
        number += 1
        
        wave_output_filename = new_file_name(musicname, 'voice' + '_' + str(number))
    
        full_wave = struct.pack('<{0}h'.format(n), *music_voice)
      
        # записываем в файл
        waveFile = wave.open(wave_output_filename, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(full_wave)  # записываем
        waveFile.close()

        choice = input('Для записи следующего файла нажмите любую клавишу;\nдля выхода из программы нажите q: ')
        if choice == 'q':
            flag = False
    
stream.stop_stream()
stream.close()
audio.terminate()
