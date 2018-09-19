import iodata as io
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import signal
import math

# Input variables
#Station = raw_input('Enter a station name (Hugo, Hylaty, Patagonia): ')
Date = raw_input('Enter date time (yyyy-mm-dd): ')
Time = raw_input('Enter time (hh-mm): ')

# Data settings
testInstance = io.InputConverter()
start = time.time()
conversionError = io.ConversionError()
data = testInstance.convert(r"/Doktorat/Python/Dane/WERA/Hylaty/{0}/".format(Date), "{0}{1}".format(Date,Time),conversionError)
end = time.time()
print("time elapsed " + str(end - start))

if(conversionError.conversionSucces):
    print("Conversion successful")
if(conversionError.conversionSucces == False):
    print("Conversion failed: " + conversionError.conversionErrorLog)
print "Done!"

# Create a new subplot for two cannals 1 & 3
a = np.amin(data.data)
Bx = data.data[0,]
By = data.data[1,]
N = len(Bx)
M = len(By)
time = np.linspace(0,300,N)
time2 = np.linspace(0,300,M)
BxTime = time[100:-100]
ByTime = time2[100:-100]

filename = 'S:/Doktorat/Python/Dane/WERA/Hylaty/{0}/{0}{1}.dat'.format(Date, Time)
d = open(filename,'rb')
degree = u"\u00b0"
headersize = 64
header = d.read(headersize)
ax1 = plt.subplot(211)
ax1.set_title(header[:16] + ', ' +                                  # station name
    'Canals: '+header[32:33]+' and '+header[34:35]+ ', '            # canals
    +'Temp'+header[38:43]+degree+'C'                                # temperature
    +', '+'Time:'+header[26:32]+', '+'Date'+' '+header[16:26])      # date

plt.ylabel('Pico Tesle [pT]')
plt.xlabel('Time [ms]')
plt.plot(BxTime, Bx[100:-100], label='Canal 1', color='r', linewidth=0.4, linestyle="-")
plt.plot(ByTime, By[100:-100], label='Canal 3', color='b', linewidth=0.4, linestyle="-")
plt.legend(loc='upper right', frameon=False, )
plt.grid()

# Create a new subplot for FFT
plt.subplot(212)
plt.title('Fast Fourier Transform')
plt.ylabel('Power [a.u.]')
plt.xlabel('Frequency Hz')
xaxis2 = np.arange(0,470,10)
plt.xticks(xaxis2)
Bxfft = (Bx[100:-100])
Byfft = (By[100:-100])
plt.grid()

# Loop for FFT data
for dataset in [Bxfft]:
    dataset = np.asarray(dataset)
    freqs, psd = signal.welch(dataset, fs=266336/300, window='hamming', nperseg=8192)
    plt.semilogy(freqs, psd/dataset.size**0, color='r')

for dataset2 in [Byfft]:
    dataset2 = np.asarray(dataset2)
    freqs2, psd2 =signal.welch(dataset2, fs=266336/300, window='hamming', nperseg=8192)
    plt.semilogy(freqs2, psd2/dataset2.size**0, color='b')

# High Pass Filter
fig2 = plt.figure(2)
plt.subplot(211)
plt.title('Butterworth High Pass Filter')
Sampling = float(266336)/300
HalfSampling = float(Sampling)/2
Wn = float(1)/HalfSampling
b, a = signal.butter(3, Wn, 'high')
BxHPF = signal.filtfilt(b, a, Bxfft)
ByHPF = signal.filtfilt(b, a, Byfft)
plt.plot(BxTime, BxHPF, label='Canal 1', color='r', linewidth=0.5, linestyle="-")
plt.plot(ByTime, ByHPF, label='Canal 3', color='b', linewidth=0.5, linestyle="-")
plt.ylabel('Pico Tesle [pT]')
plt.xlabel('Time [ms]')
plt.legend(loc='upper right', frameon=False, )
plt.grid()

# Band Stop Filter
plt.subplot(212)
f0 = 50.0
w0 = f0/(float(Sampling)/2)
Q = 30
c, d = signal.iirnotch(w0, Q)
BxBF = signal.filtfilt(d, a, BxHPF)
ByBF = signal.filtfilt(d, a, ByHPF)
plt.plot(BxTime, BxBF, label='Canal 1', color='r', linewidth=0.5, linestyle="-")
plt.plot(ByTime, ByBF, label='Canal 3', color='b', linewidth=0.5, linestyle="-")
plt.grid()
plt.show()

''''# Arcus tangens directions
with open("output.txt", "w") as f:
    result = [math.degrees(float(x)/float(y))*(-1) for x,y in zip(BxHPF,ByHPF)]
    f.write("\n".join([str(i) for i in result]))'''
