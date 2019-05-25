import wave, struct
wav_file = wave.open('task1.wav')
params = wav_file.getparams()
n = wav_file.getnframes()
data = wav_file.readframes(n)
frames = struct.unpack('<{0}h'.format(n), data)
wav_file.close()

new_frames = []
for frame in frames:
    new_frames.append(frame * 10)
new_frames = reversed(new_frames)

new_data = struct.pack('<{0}h'.format(n), *new_frames)

result_file = wave.open('result.wav', 'wb')
result_file.setparams(params)
result_file.writeframes(new_data)
result_file.close()
