import struct, pyaudio, wave

# Generate filename
def new_file_name(oldname, filtername):
    list_file_name = oldname.split('.')
    return list_file_name[0] + '_' + filtername + '.' + list_file_name[1]

# define audio format
FORMAT = pyaudio.paInt16  # sound depth = 16 bits = 2 bytes
CHANNELS = 1  # mono
RATE = 48000  # sampling frequency
CHUNK = 4000  # number of frames per query
RECORD_SECONDS = 10  # recording duration
RECORD_LEN = 5

audio = pyaudio.PyAudio()

# Open stream for reading data from micro and set params
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Open stream for output data with same params
out_stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)
flag = True
number = 1

# Wait for user to say something and start recording
while flag:
    print('say anything to start recording')

    rec_new = -1
    frames = []

    for i in range(RECORD_SECONDS):
        s = 0  # counts per secong
    
        # для каждого "запроса"
        for j in range(RATE // CHUNK):  # queries per secong
    
            data = stream.read(CHUNK)  # reading byte string
            current_frames = struct.unpack("<" + str(CHUNK) + "h", data)
    
            # sum counts modules
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
                        
                        frames += current_frames  # add read counts to the list
            else:
                if rec_new >= 0 and i < rec_end:
                    
                    frames += current_frames  # add read counts to the list
     
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
