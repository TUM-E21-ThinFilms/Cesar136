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

from e21_util.interface import Loggable

from cesar136.raw_message_packet import MessagePacket
from cesar136.constants import *
from cesar136.data_structure import *


class Command:
    def __init__(self, id, input_parameters: List[AbstractInput] = None, output_parameters: List[AbstractData] = None):
        self._id = id
        self._input = input_parameters
        self._output = output_parameters

    def get_expected_response_data_length(self):
        return sum(map(lambda x: x.get_length(), self._output))

    def get_data_config(self):
        return self._output

    def get_raw(self):
        data = []

        for input in self._input:
            data.extend(input.get())

        bytes_to_send = len(self._data)

        return MessagePacket().createMessagePacket(self._id, bytes_to_send, data)


class Driver(Loggable):
    def __init__(self, protocol, logger):
        super(Driver, self).__init__(logger)
        assert isinstance(protocol, Protocol)

    def turn_off(self):
        return self._protocol.execute(Command(1, [], []))

    def turn_on(self):
        return self._protocol.execute(Command(2, [], []))

    def set_regulation_mode(self, mode):
        mode_input = IntegerInput(mode, ParamInfos.RegulationMode)
        return self._protocol.execute(Command(3, [mode_input], []))

    def set_forward_power_limit(self, power_limit):
        power_input = IntegerInput(power_limit, ParamInfos.ForwardPowerLimit)
        return self._protocol.execute(Command(4, [power_input], []))

    def set_reflected_power_limit(self, power_limit):
        power_input = IntegerInput(power_limit, ParamInfos.ReflectedPowerLimit)
        return self._protocol.execute(Command(5, [power_input], []))

    def set_power(self, power):
        power_input = IntegerInput(power, ParamInfos.PowerSetPoint)
        return self._protocol.execut(Command(8, [power_input], []))

    def set_time_limit(self, time_limit):
        time_input = IntegerInput(time_limit, ParamInfos.RFOnTimeLimit)
        return self._protocol.execute(Command(10, [time_input], []))

    def set_control_mode(self, control_mode):
        control_input = IntegerInput(control_mode, ParamInfos.ActiveControlMode)
        return self._protocol.execute(Command(14, [control_input], []))


class presetCommands():
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
