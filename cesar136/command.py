from CeasarCommunication import MessagePacket
from CodesnBitFlags import *


class stringByte(object):
    def __init__(self, NumberOfBytes):
        self._numberOfBytes = NumberOfBytes

    def analyze(self, Intlist):
        return bytearray(Intlist, byteorder="little").decode()


class IntByte(object):
    def __init__(self, NumberOfBytes):
        self._numberOfBytes = NumberOfBytes

    def analyze(self, Intlist):
        return int.from_bytes(Intlist, byteorder="little")


class CodeByte(object):
    def __init__(self, mapping):
        self._mapping = mapping

    def analyze(self, DataInt):
        if not DataInt in self._mapping:
            raise ValueError("Ceasar unit returned different value than expected")
        return self._mapping[DataInt]


class BitFlagByte(object):
    def __init__(self, BitFlagList):  # [RESERVED, RESERVED, RECIPE_IS_ACTIVE, ...]
        self._bitFlagList = BitFlagList

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
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber)


turnOutputOff = Command(1, 0, 1)

reportPowerSupplyType = Command(128, 0, 5, [stringByte(5)])
reportModelNumber = Command(129, 0, 5, [stringByte(5)])
reportRFRampOnOff = Command(151, 0, 4, [IntByte(2), IntByte(2)])

reportReflectedPowerParameters = Command(152, 0, 3, [IntByte(1), IntByte(2)])

reportRegulationMode = Command(154, 0, 1, [CodeByte({6: FORWARD_POWER,
                                                     7: LOAD_POWER,
                                                     8: EXTERNAL_POWER})])

reportActiveControlMode = Command(155, 0, 1, [CodeByte({2: HOST_PORT,
                                                        4: USER_PORT,
                                                        6: FRONT_PANEL})])
