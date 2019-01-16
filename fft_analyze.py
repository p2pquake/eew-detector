import os
import sys
import wave
import numpy as np

# ch:          1
# bit:         8
# sample rate: 8000

# FFT window
N = 1024

# Keep "detected" status
FREEZE_COUNT = int(8000 / N * 10)

# -----------------------------------
# Initialize answer data
# -----------------------------------
def load_wave(filename):
    array = []
    with wave.open(filename, mode='rb') as f:
        while True:
            data = np.frombuffer(f.readframes(N), dtype='b')
            if len(data) < N:
                break
            fft_data = np.fft.fft(data)
            fft_abs = np.abs(fft_data)
            array.append(fft_abs)
    return np.array(array)

fft_chime = load_wave('./baseFFTs.wav')
fft_voice = load_wave('./baseAnnFFT3.wav')

# print(len(fft_chime))
# print(len(fft_voice))
fft_size = max(len(fft_chime), len(fft_voice))
# print(fft_size)

# np.set_printoptions(precision=0)
# np.set_printoptions(suppress=True)
# np.set_printoptions(linewidth=480)


# -----------------------------------
# Calculate score
# -----------------------------------
def calc_score(fft_chime, ring_fft_buffers, index):
    ring_size = len(ring_fft_buffers)
    chime_size = len(fft_chime)
    start_index = (index + (ring_size - chime_size) + 1) % ring_size 
    diff = 0
    for var in range(0, chime_size):
        #diff += np.linalg.norm(np.take(fft_chime, var, axis=0) - np.take(ring_fft_buffers, (index+var)%ring_size, axis=0))
        diff += np.linalg.norm(np.take(fft_chime, var, axis=0) - ring_fft_buffers[(start_index+var)%ring_size])
    return diff

# -----------------------------------
# Read infinite
# -----------------------------------
read_pipe = os.fdopen(sys.stdin.fileno(), 'rb', buffering=N)

index = 0
ring_fft_buffers = [0] * fft_size # np.zeros((fft_size, N))

chime_remain = 0
voice_remain = 0

while True:
    data = np.frombuffer(read_pipe.read(N), dtype='b')
    fft_data = np.fft.fft(data)
    fft_abs = np.abs(fft_data)
    ring_fft_buffers[index] = fft_abs
    #print(index)
    if chime_remain == 0:
        score = calc_score(fft_chime, ring_fft_buffers, index)
        print(score)
        if score < 1000000:
            print("*** EEW chime detected! ***")
            chime_remain = FREEZE_COUNT
    elif voice_remain == 0:
        score = calc_score(fft_voice, ring_fft_buffers, index)
        print(score)
        if score < 600000:
            print("*** EEW voice detected! ***")
            voice_remain = FREEZE_COUNT

    if chime_remain > 0:
        chime_remain -= 1
    if voice_remain > 0:
        voice_remain -= 1

    index = (index + 1) % fft_size


