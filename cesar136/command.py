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

from cesar136.raw_message_packet import MessagePacket
from cesar136.CodesnBitFlags import *
from cesar136.data_structure import *


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

        if self._DataBytesToSend > 0:
            self._DataInput = []
            sendByteCount = 0
            while sendByteCount<self._DataBytesToSend:
                try:
                    sendByteCount+=self._DataConfig[0]._byte_length
                    self._DataInput.append(self._DataConfig.pop(0))
                except:
                    break


    def set_data(self, data):
        # command is used to set data as ._DataInput defines it
        self._dataArray = []
        if len(data) != len(self._DataInput):
            raise ValueError("Not enough or too many input parameters. Input as [data1,data2]")
        for inputFormat, daten in zip(self._DataInput, data):
            if isinstance(daten, tuple):
                # not usually the case. command 29 requires bitwise input and
                # daten should be a tuple of all the bits to set to 1
                # -> convert daten to an integer
                temp = 0
                for kl in daten:
                    temp += 1 << kl
                daten = temp

            if len(inputFormat._range) == 2:
                # range consists of upper and lower boundary values
                if not daten in range(inputFormat._range[0], inputFormat._range[1]):
                    raise ValueError("input data is not allowed for this parameter. {}".format(
                        inputFormat._information))
            elif inputFormat._range:
                # range is a tuple of allowed values
                if not daten in inputFormat._range:
                    raise ValueError("input data is not allowed for this parameter. {}".format(
                        inputFormat._information))
            else:
                # range can not be easily specified accept all values...
                pass
            self._dataArray += daten.to_bytes(inputFormat._byte_length, byteorder="little")

        self._data = int.from_bytes(self._dataArray, byteorder="little")

    def prepareInteraction(self):
        if self._DataBytesToSend != 0:
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber,
                                                                 self._DataBytesToSend,
                                                                 self._data)
        else:
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber,
                                                                 self._DataBytesToSend)


turnOutputOff = Command(1, 0, 1)

setReflectedPowerParameters = Command(33,3,1,[SecondsToRFTurnOff,PowerLimitTriggerInW])


reportPowerSupplyType = Command(128, 0, 5, [StringData(5)])
reportModelNumber = Command(129, 0, 5, [StringData(5)])
reportRFRampOnOff = Command(151, 0, 4, [IntegerData(2, Parameter.RAMP_ON),
                                        IntegerData(2, Parameter.RAMP_OFF)])

reportReflectedPowerParameters = Command(152, 0, 3, [IntegerData(1, Parameter.TIME_LIMIT_RF_TURN_OFF),
                                                     IntegerData(2, Parameter.POWER_LIMIT_TRIGGER)])

reportRegulationMode = Command(154, 0, 1, [MappingData({6: Parameter.FORWARD_POWER,
                                                        7: Parameter.LOAD_POWER,
                                                        8: Parameter.EXTERNAL_POWER})])

reportActiveControlMode = Command(155, 0, 1, [MappingData({2: Parameter.HOST_PORT,
                                                           4: Parameter.USER_PORT,
                                                           6: Parameter.FRONT_PANEL})])

reportProcessStatus = Command(162, 0, 4, [ByteFlagData()] * 4)

reportSetPointAndRegulationMode = Command(164, 0, 3, [IntegerData(2, Parameter.SET_POINT_VALUE),
                                                      MappingData({6: Parameter.FORWARD_POWER,
                                                                   7: Parameter.LOAD_POWER,
                                                                   8: Parameter.EXTERNAL_POWER})])

reportForwardPower = Command(165, 0, 2, [IntegerData(2)])

reportReflectedPower = Command(166, 0, 2, [IntegerData(2)])

reportDeliveredPower = Command(167, 0, 2, [IntegerData(2)])

reportForwardPowerLimit = Command(169, 0, 2, IntegerData(2))

reportReflectedPowerLimit = Command(170, 0, 2, [IntegerData(2)])

# TODO data insertion handling
reportRecipeStepRampTime = Command(191, 1, 4, [IntegerData(2)])

reportPulsingFrequency = Command(193, 0, 4, IntegerData(4))

reportPulsingDutyCycle = Command(196, 0, 2, [IntegerData(2)])

reportUnitRunTime = Command(205, 0, 4, [IntegerData(4)])

reportSerialPortAddressAndBaudRate = Command(212, 0, 3, [IntegerData(1, Parameter.AE_BUS_ADRESS),
                                                         IntegerData(2, Parameter.BAUD_RATE)])

reportFaultStatusRegister = Command(223, 0, 4, [ByteFlagData()] * 4)

reportRFOnTimeLimit = Command(243, 0, 2, [IntegerData(2)])
