import wave, struct

# Open and read .wav file
wav_file = wave.open('task1.wav')
params = wav_file.getparams()
n = wav_file.getnframes()
data = wav_file.readframes(n)
frames = struct.unpack('<{0}h'.format(n), data)
wav_file.close()

# Create new frames
new_frames = []

# Make every sound higher
for frame in frames:
    new_frames.append(frame * 10)

# Reverse file
new_frames = reversed(new_frames)

new_data = struct.pack('<{0}h'.format(n), *new_frames)

# Write result to new .wav file
result_file = wave.open('result.wav', 'wb')
result_file.setparams(params)
result_file.writeframes(new_data)
result_file.close()
