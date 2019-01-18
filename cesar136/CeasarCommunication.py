# String of form: Header/ Command Number/ Optional Length byte/ Data/ Checksum

# def split_comstring(seq, length=8):
#     return [seq[i:i+length] for i in range(0, len(seq), length)]

CesarSerialNumber = 1  # defined by the Cesar unit used


def XorBinaries(ListOfBinaries):
    bin1 = ListOfBinaries[0]
    for k in range(len(ListOfBinaries) - 1):
        binTemp = ""
        bin2 = ListOfBinaries[k + 1]
        if len(bin1) != len(bin2):
            print("Cannot compare binaries of different format")
        else:
            for l in range(len(bin1)):
                if bin1[l] == bin2[l]:
                    x = "0"
                else:
                    x = "1"
                binTemp += x
        bin1 = binTemp
    return binTemp


def binString(Integer):
    return bin(Integer).split("b")[1]


def IntToBytearray(Int):
    result = None
    k = 0
    while result == None:
        try:
            result = bytearray(Int.to_bytes(k, "little"))
        except:
            k += 1
    return result


def createEightBitBin(int):
    return binString(int).zfill(8)


class MessagePacket():

    def __init__(self, ByteArray=[]):
        # initialize the Byte array containing the message packet.
        # empty Array if Message packet is to be created
        self.ByteArray = ByteArray
        # every element for the message has two different entries( int and bin)
        # should be accessed and written to this order: [Int, Bin]
        self.Header = [None] * 2
        self.CommandNumber = [None] * 2
        self.OptionalLengthByte = [None] * 2
        self.Checksum = [None] * 2
        self.IntBinArray = [None] * 2
        # Data is stored in a byte and a bin array with little endian, first component is the actual int value:
        # [int,[byte,byte,byte],[bin,bin,bin]
        self.Data = [None] * 3
        self.lenData = 0
        self.DataLong = False

    def splitUpPacket(self):
        if self.ByteArray:
            self.Header[0] = self.ByteArray.pop(0)
            self.Header[1] = createEightBitBin(self.Header[0])
            self.CommandNumber[0] = self.ByteArray.pop(0)  # command number from 0-255
            # if more than 6 Data bytes, the string contains an optional length byte
            # maximum bytes left when no optional length string needed are 7
            if len(self.ByteArray) > 7:
                self.DataLong = True
                self.OptionalLengthByte[0] = self.ByteArray.pop(0)
            self.Checksum[0] = self.ByteArray.pop()
            self.lenData = len(self.ByteArray)
            self.Data[1] = self.ByteArray
            self.Data[0] = int.from_bytes(self.ByteArray, byteorder="little")
            self.createIntBinArray()

    def calculateChecksum(self):
        self.Checksum[1] = XorBinaries(self.IntBinArray[1])
        self.Checksum[0] = int(self.Checksum[1], 2)
        for k in range(2):
            self.IntBinArray[k].append(self.Checksum[k])

    def createIntBinArray(self):
        #  due to different structure self.Header bin is calculated in self.createHeader()
        self.CommandNumber[1] = createEightBitBin(self.CommandNumber[0])
        for k in range(2):
            self.IntBinArray[k] = [self.Header[k], self.CommandNumber[k]]
            if self.DataLong:
                self.OptionalLengthByte[1] = createEightBitBin(self.OptionalLengthByte[0])
                self.IntBinArray[k].append(self.OptionalLengthByte[k])
            if self.lenData != 0:
                #
                self.Data[2] = [createEightBitBin(kl) for kl in self.Data[1]]
                self.IntBinArray[k] += self.Data[k + 1]

    def createHeader(self, datalength, serialnumber):
        serialBinString = binString(serialnumber).zfill(5)
        datalengthBinstring = binString(datalength).zfill(3)
        self.Header[1] = serialBinString + datalengthBinstring
        self.Header[0] = int(self.Header[1], 2)

    def createMessagePacket(self, CommandInput, DataInput=-1):
        self.CommandNumber[0] = int(CommandInput)
        self.Data[0] = int(DataInput)
        if DataInput != -1:
            self.Data[1] = IntToBytearray(self.Data[0])
            # TODO self.lenData auch in Split up
            self.lenData = len(self.Data[1])
            if self.lenData > 6:
                self.DataLong = True
                self.OptionalLengthByte[0] = self.lenData
                self.createHeader(7, CesarSerialNumber)
        if self.lenData < 7:
            self.createHeader(self.lenData, CesarSerialNumber)
        self.assembleMessagePacket()
        return self.IntBinArray

    def assembleMessagePacket(self):
        # assembles every component of the message, calculates the Checksum and
        self.createIntBinArray()
        self.calculateChecksum()
        self.ByteArray = bytearray(self.IntBinArray[0])


class ReceivedByteArray(MessagePacket):

    def __init__(self, ByteArray):
        MessagePacket.__init__(self, ByteArray)
        MessagePacket.splitUpPacket(self)

    def extractData(self, DataConfig):
        self.formatedData = []
        self.DataRanges = DataConfig[0]
        self.DataRangesFormat = DataConfig[1]
        lastByte = 0
        for k in range(len(self.DataRanges)):
            if self.DataRangesFormat[k] == 0:
                # data format is an integer
                data = int.from_bytes(self.Data[1][lastByte:self.DataRanges[k]], byteorder="little")
            elif self.DataRangesFormat[k] == 1:
                # data format is a certain code
                pass
            elif self.DataRangesFormat[k] == 2:
                # dataformat is a string
                data = self.Data[1][lastByte:self.DataRanges[k]].decode()
            self.formatedData.append(data)
            lastByte = self.DataRanges[k]

    def checkForCompletness(self):
        self.Checksum[1] = createEightBitBin(self.Checksum[0])
        self.IntBinArray[1].append(self.Checksum[1])
        result = 0
        XorBin = XorBinaries(self.IntBinArray[1])
        for r in XorBin:
            result += int(r)
        return result

    def getCesarAddress(self):
        # The address of the Unit to talk to and talking to the host is in the 4th to \
        # 8th bit of the header
        Binadress = self.Header[1][0:5]
        return int(Binadress, 2)

# x=MessagePacket()
# r=x.createMessagePacket(1)
# s=MessagePacket()
# f=s.createMessagePacket(129)
# kl=MessagePacket().createMessagePacket(125)
#
# print(kl)
