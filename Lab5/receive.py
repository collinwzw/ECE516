import sounddevice as sd
import matplotlib.pyplot as plt
fs = 1000
recording = []
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata
    recording.append(indata)
    #print(len(recording))
    #plt.plot(recording)
print(sd.query_devices())

try:
    with sd.Stream(device=(0,3), samplerate=fs, dtype='float32', latency=None, channels=1, callback=callback):
        input()

except KeyboardInterrupt:
    pass
