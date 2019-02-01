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

from cesar136.CeasarCommunication import MessagePacket
from cesar136.CodesnBitFlags import *

# any additional new datatype has to contain the instance _numberOfBytes
# and the function analyze()

class StringData(object):
    def __init__(self, NumberOfBytes):
        self._numberOfBytes = NumberOfBytes

    def analyze(self, Intlist):
        # get rid of empty bytes
        Intlist = [k for k in Intlist if k != 0]
        return bytearray(Intlist).decode()


class IntegerData(object):
    def __init__(self, NumberOfBytes):
        self._numberOfBytes = NumberOfBytes

    def analyze(self, Intlist):
        return int.from_bytes(Intlist, byteorder="little")


class MappingData(object):
    def __init__(self, mapping):
        self._mapping = mapping
        self._numberOfBytes = 1

    def analyze(self, DataInt):
        if not DataInt in self._mapping:
            raise ValueError("Ceasar unit returned different value than expected")
        return self._mapping[DataInt]


class ByteFlagData(object):
    def __init__(self, BitFlagList):  # [RESERVED, RESERVED, RECIPE_IS_ACTIVE, ...]
        self._bitFlagList = BitFlagList
        self._numberOfBytes = 1

    def get_flag(self, bit_position):
        pass


class Command():
    def __init__(self, commandNumber, DataBytesTosend, DatabytesExpected, DataConfig=None):
        self._commandNumber = commandNumber
        self._DataBytesToSend = DataBytesTosend
        self._DataBytesExpected = DatabytesExpected
        if self._commandNumber < 128:
            self._CSRonly = True
        else:
            self._CSRonly = False
            self._DataConfig = DataConfig

    def set_data(self, data):
        self._data = data

    def prepareInteraction(self):
        if self._DataBytesToSend != 0:
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber,
                                                                 self._DataBytesToSend,
                                                                 self._data)
        else:
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber,
                                                                 self._DataBytesToSend)


turnOutputOff = Command(1, 0, 1)

reportPowerSupplyType = Command(128, 0, 5, [StringData(5)])
reportModelNumber = Command(129, 0, 5, [StringData(5)])
reportRFRampOnOff = Command(151, 0, 4, [IntegerData(2), IntegerData(2)])

reportReflectedPowerParameters = Command(152, 0, 3, [IntegerData(1), IntegerData(2)])

reportRegulationMode = Command(154, 0, 1, [MappingData({6: FORWARD_POWER,
                                                        7: LOAD_POWER,
                                                        8: EXTERNAL_POWER})])

reportActiveControlMode = Command(155, 0, 1, [MappingData({2: HOST_PORT,
                                                           4: USER_PORT,
                                                           6: FRONT_PANEL})])
