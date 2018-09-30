import iodata as io
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import csv

# Input variables
h = "Hylaty"
u = 'Hugo'
p = 'Patagonia'

Station = input('Enter a station name (Hylaty = h, Hugo = u, Patagonia = p): ')
Date = raw_input('Enter date time (yyyymmdd): ')
Date_end = raw_input('Enter end date time (yyyymmdd): ')
Start_time_hours = int(raw_input('Enter start time (hh): '))
Start_time_minutes = int(raw_input('Enter start time (mm): '))
End_time_hours = int(raw_input('Enter end time (hh): '))
End_time_minutes = int(raw_input('Enter end time (mm): '))
Save_Print_SavPrin = raw_input('Press s = Save, p = Plot: ')

class DataVariables():
    def __init__(self, datamatrix):
        np.amin(data.data)
        self.datamatrix = datamatrix[100:-100]
        self.matrixtime = np.linspace(0, 300, len(datamatrix))
        self.time = self.matrixtime[100:-100]

class Charts(DataVariables):
    def __init__(self, datamatrix, plot_label, line_color):
        DataVariables.__init__(self, datamatrix)
        plt.ylabel('Pico Tesle [pT]')
        plt.xlabel('Time [ms]')
        plt.plot(self.time, self.datamatrix, label=plot_label, color=line_color, linewidth=0.4, linestyle="-")

class SignalChart(DataVariables):
    def __init__(self, datamatrix,plot_label, line_color):
        DataVariables.__init__(self, datamatrix)
        self.samples = float(266336)/300
        self.halfsamples = float(self.samples)/2
        self.Wn = float(1)/self.halfsamples
        b, a = signal.butter(3, self.Wn, 'high')
        self.signal = signal.filtfilt(b, a, self.datamatrix)
        plt.title('Butterworth High Pass Filter')
        plt.plot(self.time, self.signal, label=plot_label, color=line_color,linewidth=0.4, linestyle="-")

    def save(self, name):
        self.datalist = list(zip(self.signal, self.matrixtime))
        self.name = name
        with open("S:\Doktorat\Python\Dane\Codes\Dipoles\{}.txt".format(name), 'w') as Peak:
            writer = csv.writer(Peak, lineterminator='\n')
            for val in [j for i, j, k in zip(self.datalist, self.datalist[1:], self.datalist[2:]) if i < j and j > k and
                            j[0] >= 100.0]:
                writer.writerow([val])

# Data settings
testInstance = io.InputConverter()
conversionError = io.ConversionError()

while Start_time_hours == Start_time_hours and Start_time_minutes == Start_time_minutes and Date == Date:

    if Start_time_hours == 23 and Start_time_minutes == 60 and Date != Date_end:
        Date = int(Date)
        Date += 1
        Date = str(Date)
        Start_time_minutes = 00
        Start_time_hours = 00

    print "********************************************************"
    Start_time_hours_format = '{:02}'.format(Start_time_hours)
    Start_time_minutes_format = '{:02}'.format(Start_time_minutes)

    print "Operating data: Station: {0}, Date: {1} {2}:{3} UTC".format(Station, Date, Start_time_hours_format,
                                                                       Start_time_minutes_format)

    Start_time_hours += (Start_time_minutes / 60)
    Start_time_minutes %= 60
    str(Start_time_minutes)
    str(Start_time_hours)
    str(End_time_minutes)
    str(End_time_hours)
    Start_time_hours_format = '{:02}'.format(Start_time_hours)
    Start_time_minutes_format = '{:02}'.format(Start_time_minutes)
    End_time_hours_format = '{:02}'.format(End_time_hours)
    End_time_minutes_format = '{:02}'.format(End_time_minutes)
    int(Start_time_minutes)
    Start_time_minutes += 5

    data = testInstance.convert(r"/Doktorat/Python/Dane/WERA/{0}/{1}/".format(Station, Date),
                                "{0}{1}{2}".format(Date, Start_time_hours_format, Start_time_minutes_format),
                                conversionError)
    filename = 'S:/Doktorat/Python/Dane/WERA/{0}/{1}/{1}{2}{3}.dat'.format(Station, Date, Start_time_hours_format,
                                                                          Start_time_minutes_format)
    d = open(filename,'rb')
    degree = u"\u00b0"
    headersize = 64
    header = d.read(headersize)
    plt.figure(figsize=(20.0, 15.0))
    fig = plt.figure(1)
    ax1 = plt.subplot(211)
    ax1.set_title(header[:16] + ', ' +                                  # station name
        'Channels: '+header[32:33]+' and '+header[34:35]+ ', '          # canals
        +'Temp'+header[38:43]+degree+'C'                                # temperature
        +', '+'Time:'+header[26:32]+', '+'Date'+' '+header[16:26])      # date

    Charts(data.data[0,], plot_label='Channel 1', line_color='r')
    Charts(data.data[1,], plot_label='Channel 3', line_color='b')
    plt.grid()

    plt.subplot(212)
    SigBx = SignalChart(data.data[0,], plot_label='Channel 1', line_color='r')
    SigBy = SignalChart(data.data[1,], plot_label='Channel 3', line_color='b')
    plt.grid()

    if Save_Print_SavPrin == "p":
        print("Showing figures...")
        plt.show()
        print "Succesful!"
        if Start_time_hours_format == End_time_hours_format and Start_time_minutes_format == End_time_minutes_format and Date == Date_end:
            break

    elif Save_Print_SavPrin == "s":
        print "Saving: I {0}{1}{2}.csv".format(Station, Start_time_hours_format, Start_time_minutes_format)
        SignalChart(data.data[0,], plot_label='Channel 1', line_color='r').save('DipoleBx ' + "{0}".format(Station) + "{0}{1}{2}".format(
                Date, Start_time_hours_format, Start_time_minutes_format))
        SignalChart(data.data[1,], plot_label='Channel 3', line_color='b').save('DipoleBy ' + "{0}".format(Station) + "{0}{1}{2}".format(
                Date, Start_time_hours_format, Start_time_minutes_format))
        fig.savefig('S:\Doktorat\Python\Dane\Codes\Dipoles\Chart ' + "{0}".format(Station) + "{0}{1}{2}".format(
            Date, Start_time_hours_format, Start_time_minutes_format) + ".png", format='png')
        plt.close(fig)
        fig.clf()

        if Start_time_hours_format == End_time_hours_format and Start_time_minutes_format == End_time_minutes_format and Date == Date_end:
            break
