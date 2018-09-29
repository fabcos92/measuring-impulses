import struct
import numpy as np

class ConversionError:
    def __init__(self):
        self.conversionSucces = True
        self.conversionErrorLog = "Poprawnie"

    def reportFailure(self, errorlog):
        self.conversionSucces = False
        self.conversionErrorLog = errorlog

class DataStruct:
    def __init__(self,data,initTime,headerString):
        self.data = data
        self.initTime = initTime
        self.headerString = headerString

class InputConverter:
    def __init__(self):
        self.midAdc = 65536/2
        self.convFactor = 19.54

    def convert(self,filePath,fileName,conversionLog):
        try:
            d_file = open(filePath + "/" + fileName + ".dat", mode='rb')
        except IOError as e:
            conversionLog.reportFailure(e.strerror)

        file = d_file.read()
        datalen = len(file)
        headerString = file[:43]
        initime, = struct.unpack('>H', file[48:50])
        expectedMatrixWidth = (datalen - 72)/4
        outputMatrix = np.zeros((2, expectedMatrixWidth))
        index = 0;
        print "Processing..."
        for i in range(64, datalen-8, 4):
            e1, e2 = struct.unpack('>HH',file[i:i+4])
            outputMatrix[0, index] = (e1 - self.midAdc)/self.convFactor
            outputMatrix[1, index] = (e2 - self.midAdc)/self.convFactor
            index += 1
            #with open('S:/Doktorat/Dane/Hugo/'+"201604010000" + ".csv" ,"w") as out_file:
                #for j in range(len(outputMatrix)):
                    #out_string = ""
                    #out_string += str(outputMatrix)
                    #out_string += "\n"
                    #out_file.write(out_string)

        return DataStruct(outputMatrix,initime,headerString)






