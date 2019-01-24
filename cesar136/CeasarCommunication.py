# String of form: Header/ Command Number/ Optional Length byte/ Data/ Checksum

# def split_comstring(seq, length=8):
#     return [seq[i:i+length] for i in range(0, len(seq), length)]

CesarSerialNumber = 1  # defined by the Cesar unit used

from command import *


def compute_checksum(binaries):
    assert isinstance(binaries, list)

    result = 0x00

    for data in binaries:
        result = int(data) ^ result

    return result


def intToBytearray(Int, NumberOfBytes):
    return bytearray(Int.to_bytes(NumberOfBytes, "little"))


class MessagePacket(object):

    def __init__(self, binary_data=[]):

        self._raw = binary_data

        self._header = 0
        self._checksum = 0
        self._command_id = 0
        self._optional_length = 0
        self._data = []

        self._address = 0
        self._lenData = 0
        self._intArray = []

    def splitUpPacket(self):
        if self._raw:
            self._header = self._raw.pop(0)
            self.splitHeader()  # splits header into address of Cesar unit and the number of data bytes
            self._command_id = self._raw.pop(0)  # command number from 0-255
            # if more than 6 Data bytes, the string contains an optional length byte
            # maximum bytes left when no optional length string needed are 7
            if len(self._raw) > 7:
                # self.DataLong = True
                self._optional_length = self._raw.pop(0)
            self._checksum = self._raw.pop()
            self._data = [k for k in self._raw]

            self.createIntArray()

    def splitHeader(self):
        self._address = self._header >> 3
        self._lenData = self._header & 0b111

    def createChecksum(self):
        self._checksum = compute_checksum(self._intArray)
        self._intArray.append(self._checksum)

    def createIntArray(self):
        # all components need to exist before calling this function
        # self._intArray contains no checksum
        self._intArray = [self._header, self._command_id]
        if self._lenData > 6:
            self._intArray.append(self._optional_length)
        if self._lenData != 0:
            self._intArray += self._data

    def createHeader(self, datalength, serialnumber):
        temp = serialnumber << 3  # shift serialnumber three bits
        self._header = temp | datalength  # insert datalength to the three bits

    def createMessagePacket(self, CommandInput, NumberOfDatabytes, DataInput=-1):
        self._command_id = CommandInput
        self._lenData = NumberOfDatabytes
        if DataInput != -1:
            temp = intToBytearray(DataInput, self._lenData)
            self._data = [k for k in temp]
            if self._lenData > 6:
                self._optional_length = self._lenData
                self.createHeader(7, CesarSerialNumber)
        if self._lenData < 7:
            self.createHeader(self._lenData, CesarSerialNumber)
        self.assembleMessagePacket()
        return self._intArray

    def assembleMessagePacket(self):
        # assembles every component of the message, calculates the Checksum and
        self.createIntArray()
        self.createChecksum()
        self.ByteArray = bytearray(self._intArray[0])


class ReceivedByteArray(MessagePacket):

    def __init__(self, binary_data):
        MessagePacket.__init__(self, binary_data)
        MessagePacket.splitUpPacket(self)

    def checkForCompletness(self):
        tempArray = self._intArray.append(self._checksum)
        return compute_checksum(tempArray)

    def extractData(self, DataConfig):
        self._formatedData = []
        index = 0
        for config in DataConfig:
            if type(config) == IntByte or stringByte:
                tempData = self._data[index:config._numberOfBytes]
                self._formatedData.append(config.analyze(tempData))
                index = config._numberOfBytes

            elif type(config) == CodeByte:
                tempData = self._data[index]
                self._formatedData.append(config.analyze(tempData))
                index += 1
            elif type(config) == BitFlagByte:
                # TODO do something
                pass

    def getCesarAddress(self):
        return self._address

    def getCommandId(self):
        return self._command_id

# x=MessagePacket()
# r=x.createMessagePacket(1)
# s=MessagePacket()
# f=s.createMessagePacket(129)
# kl=MessagePacket().createMessagePacket(125)
#
# print(kl)
