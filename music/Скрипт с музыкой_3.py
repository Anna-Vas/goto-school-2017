import wave, struct
wav_file = wave.open('task1.wav')
params = wav_file.getparams()
n = wav_file.getnframes()
data = wav_file.readframes(n)
frames = struct.unpack('<{0}h'.format(n), data)
wav_file.close()

new_frames = []
for frame in frames[::-100]:
    new_frames.append(frame * 10)

new_data = struct.pack('<{0}h'.format(len(new_frames)), *new_frames)

result_file = wave.open('result3.wav', 'wb')
result_file.setparams(params)
result_file.writeframes(new_data)
result_file.close()
