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
            while sendByteCount < self._DataBytesToSend:
                try:
                    sendByteCount += self._DataConfig[0]._byte_length
                    self._DataInput.append(self._DataConfig.pop(0))
                except:
                    break

    def set_data(self, data):
        # command is used to set data as ._DataInput defines it
        self._dataArray = []
        if len(data) != len(self._DataInput):
            raise ValueError("Not enough or too many input parameters. Input as [data1,data2]")
        for inputFormat, daten in zip(self._DataInput, data):
            if inputFormat._range is not None:
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

class presetCommands():
    # command 1
    turnOutputOff = Command(1, 0, 1)

    # command 2
    turnOutputOn = Command(2, 0, 1)

    # command 3
    setRegulationMode = Command(3, 1, 1, [ParamInfos.RegulationMode])

    # command 4
    setForwardPowerLimit = Command(4, 2, 1, [ParamInfos.ForwardPowerLimit])

    # command 5
    setReflectedPowerLimit = Command(5, 2, 1, [ParamInfos.ReflectedPowerLimit])

    # command 8
    setPowerSetPoint = Command(8, 2, 1, [ParamInfos.PowerSetPoint])

    # command 10
    setRFOnTimeLimit = Command(10, 2, 1, [ParamInfos.RFOnTimeLimit])

    # command 14
    setActiveControlMode = Command(14, 1, 1, [ParamInfos.ActiveControlmode])

    # command 19
    setNumberOfRecipeSteps = Command(19, 1, 1, [ParamInfos.NumberOfRecipeSteps])

    # command 21
    setRecipeStepRampTime = Command(21, 3, 1, [ParamInfos.RecipeStepNumber, ParamInfos.RecipeRampRunTime])

    # command 22
    setStepSetPoint = Command(22, 3, 1, [ParamInfos.RecipeStepNumber, ParamInfos.PowerStepSetPoint])

    # command 23
    setRecipeStepRunTime = Command(23, 3, 1, [ParamInfos.RecipeStepNumber, ParamInfos.RecipeRampRunTime])

    # command 24
    savePresets = Command(24, 1, 1, [ParamInfos.PresetsNumber])

    # command 25
    restorePresets = Command(25, 1, 1, [ParamInfos.PresetsNumber])

    # command 29
    setRemoteControlOverride = Command(29, 1, 1, [ParamInfos.RemoteControlOverride])

    # command 30
    setUserPortScaling = Command(30, 1, 1, [ParamInfos.UserPortScaling])

    # command 31
    setRFOnOffRampingRiseTime = Command(31, 2, 1, [ParamInfos.RampRiseFallTime])

    # command 32
    setRFOnOffRampingFallTime = Command(32, 2, 1, [ParamInfos.RampRiseFallTime])

    # command 33
    setReflectedPowerParameters = Command(33, 3, 1, [ParamInfos.SecondsToRFTurnOff, ParamInfos.PowerLimitTriggerInW])

    # command 69
    setSerialBaudRate = Command(69, 3, 1, [ParamInfos.IgnoredByte, ParamInfos.BaudRate])

    # command 93
    setPulsingFrequency = Command(93, 4, 1, [ParamInfos.PulsingFrequency])

    # command 96
    setPulsingDutyCycle = Command(96, 2, 1, [ParamInfos.PulsingDutyCycle])

    # command 128
    reportPowerSupplyType = Command(128, 0, 5, [StringData(5)])

    # command 129
    reportModelNumber = Command(129, 0, 5, [StringData(5)])

    # command 151
    reportRFRampOnOff = Command(151, 0, 4, [IntegerData(2, Parameter.RAMP_ON),
                                            IntegerData(2, Parameter.RAMP_OFF)])

    # command 152
    reportReflectedPowerParameters = Command(152, 0, 3, [IntegerData(1, Parameter.TIME_LIMIT_RF_TURN_OFF),
                                                         IntegerData(2, Parameter.POWER_LIMIT_TRIGGER)])

    # command 154
    reportRegulationMode = Command(154, 0, 1, [MappingData({6: Parameter.FORWARD_POWER,
                                                            7: Parameter.LOAD_POWER,
                                                            8: Parameter.EXTERNAL_POWER})])

    # command 155
    reportActiveControlMode = Command(155, 0, 1, [MappingData({2: Parameter.HOST_PORT,
                                                               4: Parameter.USER_PORT,
                                                               6: Parameter.FRONT_PANEL})])

    # command 162
    reportProcessStatus = Command(162, 0, 4, [ByteFlagData()] * 4)

    # command 164
    reportSetPointAndRegulationMode = Command(164, 0, 3, [IntegerData(2, Parameter.SET_POINT_VALUE),
                                                          MappingData({6: Parameter.FORWARD_POWER,
                                                                       7: Parameter.LOAD_POWER,
                                                                       8: Parameter.EXTERNAL_POWER})])

    # command 165
    reportForwardPower = Command(165, 0, 2, [IntegerData(2)])

    # command 166
    reportReflectedPower = Command(166, 0, 2, [IntegerData(2)])

    # command 167
    reportDeliveredPower = Command(167, 0, 2, [IntegerData(2)])

    # command 169
    reportForwardPowerLimit = Command(169, 0, 2, [IntegerData(2)])

    # command 170
    reportReflectedPowerLimit = Command(170, 0, 2, [IntegerData(2)])

    # command 191
    reportRecipeStepRampTime = Command(191, 1, 4, [ParamInfos.RecipeStepNumber, IntegerData(2)])

    # command 193
    reportPulsingFrequency = Command(193, 0, 4, IntegerData(4))

    # command 196
    reportPulsingDutyCycle = Command(196, 0, 2, [IntegerData(2)])

    # command 205
    reportUnitRunTime = Command(205, 0, 4, [IntegerData(4)])

    # command 212
    reportSerialPortAddressAndBaudRate = Command(212, 0, 3, [IntegerData(1, Parameter.AE_BUS_ADRESS),
                                                             IntegerData(2, Parameter.BAUD_RATE)])

    # command 223
    reportFaultStatusRegister = Command(223, 0, 4, [ByteFlagData()] * 4)

    # command 243
    reportRFOnTimeLimit = Command(243, 0, 2, [IntegerData(2)])
