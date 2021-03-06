"""Pass input directly to output.

https://app.assembla.com/spaces/portaudio/git/source/master/test/patest_wire.c

"""
import argparse
import queue
import sys
import time as tl
from datetime import datetime
import sounddevice as sd
import numpy as np  # Make sure NumPy is loaded before it is used in the callback
from scipy.signal import butter, lfilter, freqz
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import scipy
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-t', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument('--dtype', help='audio data type')
parser.add_argument('--samplerate', type=float, help='sampling rate')
parser.add_argument('--blocksize', type=int, help='block size')
parser.add_argument('--latency', type=float, help='latency in seconds')
args = parser.parse_args(remaining)

if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1

#Buffer for feeding samples to plot
q = queue.Queue()
i=0
#Indexing variable for generating the sine wave sound
start_idx = 0
order = 10
starting_time = 0
endtime = 0

sampling_freq = 44100

cutoff_freq = 50

sampling_duration = 1
avg = []
number_of_samples = sampling_freq * sampling_duration
normalized_cutoff_freq = 2 * cutoff_freq / sampling_freq
numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff_freq,btype='lowpass')
def Average(lst):
    return sum(lst) / len(lst)
def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    global i, avg, starting_time
    while True:
        try:
            data = q.get_nowait()
            data = np.amax(data)
            #print(data)
            if len(avg)>= 10 and data > 10 * Average(avg):
                endtime = tl.time()
                print("different frequency detected")
                print("time difference = " + str(endtime - starting_time) )
            else:
                avg.append(data)


        except queue.Empty:
            break
        #data = np.average(data)
        shift = 1
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines

try:
    length = int(200 * args.samplerate / (1000 * 10))
    plotdata = np.zeros((length, len(args.channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend(['channel {}'.format(c) for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    ax.axis((0, len(plotdata), -1e-2, 1e-2))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    def callback(indata, outdata, frames, time, status):
        global i, starting_time
        if status:
            print(status)
        global start_idx
        #frames = frames/2
        #Generate the sine wave for output
        t = (start_idx + np.arange(frames)) /  args.samplerate
        t = t.reshape(-1, 1)
        #outdata[:] = np.sin(0)
        if i == 100:
            outdata[:] = np.cos(44100 * t)
            starting_time = tl.time()
        else:
            outdata[:] = np.cos(1000 * t)
        i=i+1
        start_idx += frames
        filtered_signal = scipy.signal.lfilter(numerator_coeffs, denominator_coeffs, outdata * indata[::1, mapping])
        #print(starting_time)
        #Plot the received microphone input
        q.put(indata[::1,mapping])

        

    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=2, callback=callback):
        plt.show()
        sys.exit()

except KeyboardInterrupt:
    parser.exit('')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
