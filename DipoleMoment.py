import iodata as io
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import signal
import csv

# Data settings
testInstance = io.InputConverter()
start = time.time()
conversionError = io.ConversionError()
data = testInstance.convert(r"/Doktorat/Python/Dane/WERA/Hylaty/20150719/", "201507191200",conversionError)
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

filename = 'S:/Doktorat/Python/Dane/WERA/Hylaty/20150719/201507191200.dat'
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

Bxfft = (Bx[100:-100])
Byfft = (By[100:-100])


# High Pass Filter
plt.subplot(212)
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

plt.show()


lst = list(zip(BxHPF, BxTime))
lst2 = list(zip(ByHPF, ByTime))

res = [j for i, j, k in zip(lst, lst[1:], lst[2:]) if i < j and j > k and j[0] >= 100.0]
res2 = [j2 for i2, j2, k2 in zip(lst2, lst2[1:], lst2[2:]) if i2 < j2 and j2 > k2 and j2[0] >= 100.0]

with open("S:\Doktorat\Python\Dane\Codes\BxHPF.txt", 'w') as Peak1:
    writer = csv.writer(Peak1, lineterminator='\n')
    for val in res:
        writer.writerow([val])

with open("S:\Doktorat\Python\Dane\Codes\ByHPF.txt", 'w') as Peak2:
    writer2 = csv.writer(Peak2, lineterminator='\n')
    for val2 in res2:
        writer2.writerow([val2])


