# Copyright (C) 2019, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# String of form: Header/ Command Number/ Optional Length byte/ Data/ Checksum

# def split_comstring(seq, length=8):
#     return [seq[i:i+length] for i in range(0, len(seq), length)]

from typing import List

#from cesar136.command import

def intToBytearray(Int, NumberOfBytes):
    return bytearray(Int.to_bytes(NumberOfBytes, "little"))


class MessagePacket(object):
    CESAR_DEFAULT_DEVICE_NUMBER = 1
    MAX_DATA_LENGTH = 0b111

    def __init__(self, binary_data=[], cesar_device_number=None):

        self._raw = binary_data

        self._header = 0
        self._checksum = 0
        self._command_id = 0
        self._optional_length = 0
        self._data = []

        self._address = 0
        self._data_length = 0
        self._intArray = []

        if cesar_device_number is None:
            cesar_device_number = self.CESAR_DEFAULT_DEVICE_NUMBER

        self._device_id = cesar_device_number

        # create all instances out of binary data if present
        if self._raw:
            self.parse_packet(binary_data)

    @classmethod
    def from_raw(cls, binary_data):
        return cls(binary_data)

    def get_header(self):
        return self._header

    def set_address(self, address):
        if not 0 <= address <= 0b11111:
            raise ValueError("Given address is invalid")

        self._address = address

    def set_data(self, data: bytearray):
        if len(data) > 255:
            raise ValueError("Cannot send more than 255 data bytes")

        self._data = data

    def set_command(self, command_id):
        if not 0 <= command_id <= 255:
            raise ValueError("Invalid command id given")

        self._command_id = command_id

    def get_data(self):
        return self._data

    def to_raw(self):
        data_length = len(self._data)

        header_data_length = data_length
        optional_length = None

        if data_length > 0b111:
            header_data_length = 0b111
            optional_length = data_length

        header = (self._address << 3) | header_data_length

        raw = [header, self._command_id, optional_length] + self._data
        # remove the optional length byte if it is None
        raw = [el for el in raw if el is not None]

        checksum = self.xor(raw)

        return raw + [checksum]

    def parse_packet(self, raw: bytearray):
        data = raw.copy()

        self._header = data.pop(0)

        self._address = self._header >> 3
        self._data_length = self._header & self.MAX_DATA_LENGTH

        self._command_id = data.pop(0)  # command number from 0-255

        # if more than 6 Data bytes, the data contains an optional length byte
        # maximum bytes left when no optional length string needed are 7
        if len(data) > 7:
            self._optional_length = data.pop(0)

        self._checksum = data.pop()
        # need for list comprehension in order to store self._data as an int list and not a bytearray
        self._data = [k for k in data]

        self.createIntArray()

    def create_header(self, datalength, serialnumber=None):
        if datalength > self.MAX_DATA_LENGTH:
            raise RuntimeError("Given data length exceeds the maximum data length")

        if serialnumber is None:
            serialnumber = self.CESAR_DEFAULT_DEVICE_NUMBER

        temp = serialnumber << 3  # shift serialnumber three bits
        self._header = temp | datalength  # insert datalength to the three bits

    def xor(self, raw: bytearray):
        result = 0

        for data in raw:
            result = int(data) ^ result

        return result

    def compute_checksum(self, raw: List[int] = None):

        if raw is None:
            raw = self._intArray

        # TODO assignment of result needed?
        result = self.xor(raw)

        self._checksum = result
        self._intArray.append(self._checksum)

    def createIntArray(self):
        # all components need to exist before calling this function
        # self._intArray contains no checksum
        self._intArray = [self._header, self._command_id]
        if self._data_length > 6:
            self._intArray.append(self._optional_length)
        if self._data_length != 0:
            self._intArray += self._data

    def createMessagePacket(self, cmd_id, data_length, data=None):
        self._command_id = cmd_id
        self._data_length = data_length

        if data is not None:
            temp = intToBytearray(data, self._data_length)
            self._data = [k for k in temp]

            if self._data_length > 6:
                self._optional_length = self._data_length
                self.create_header(7, self._device_id)

        if self._data_length < 7:
            self.create_header(self._data_length, self._device_id)

        self.assembleMessagePacket()
        return self._intArray

    def assembleMessagePacket(self):
        # assembles every component of the message, calculates the Checksum and
        self.createIntArray()
        self.compute_checksum()
        self.ByteArray = bytearray(self._intArray)


class ReceivedByteArray(MessagePacket):

    def __init__(self, binary_data):
        super(ReceivedByteArray, self).__init__(binary_data)

    def checkForCompletness(self):
        # returns the xor value for the complete received package
        # using compute_checksum() to append checksum to _intArray
        # any return other than zero indicates an incomplete message
        self.compute_checksum()
        return self.xor(self._intArray)

    def extractData(self, DataConfig):
        self._formatedData = []
        index = 0

        data = ResponseValue()

        for config in DataConfig:
            end_Of_Data = index + config._numberOfBytes
            tempData = self._data[index:end_Of_Data]
            config.set_data(tempData)
            data.set_parameter(config) #.analyze(tempData))
            #self._formatedData.append(config.analyze(tempData))
            index = end_Of_Data

        return data

    def getCesarAddress(self):
        return self._address

    def getCommandId(self):
        return self._command_id


class AbstractData(object):
    def __init__(self, name=''):
        self._name = name
        self._data = None

    def get_name(self):
        return self._name

    def set_data(self, data):
        self._data = data

class ResponseValue(object):
    def __init__(self):
        self._params = []

    def set_parameter(self, data: AbstractData):
        self._params.append(data)

    def get_parameter(self, name=''):

        if len(self._params) == 1:
            return self._params[0]

        for el in self._params:
            if el.get_name() == name:
                return el

        raise RuntimeError("Could not find given parameter {}".format(name))

# x=MessagePacket()
# r=x.createMessagePacket(1)
# s=MessagePacket()
# f=s.createMessagePacket(129)
# kl=MessagePacket().createMessagePacket(125)
#
# print(kl)
