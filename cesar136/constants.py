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

class ValidationError(RuntimeError):
    pass

class InputParam():
    def __init__(self, information, position, length, expected_values=None):
        self._information = information
        self._postion = position
        self._byte_length = length
        self._range = expected_values

    def validate(self, data):
        if self._range is None:
            return

        if data not in self._range:
            raise ValidationError(self._information)

    def get_length(self):
        return self._byte_length

class ParamInfos():
    # command 3
    RegulationMode = InputParam("accepts only these specific values \n"
                                "6, Forward power regulation\n"
                                "7, Load power regulation (also called real or delivered power)\n"
                                "8, External power regulation (DC Bias)\n",
                                0, 1, (6, 7, 8))

    # command 4
    ForwardPowerLimit = InputParam("accepts a value of 5 to 100 percent of maximum power",
                                   0, 2)  # TODO find out range(maximum power)

    # command 5
    ReflectedPowerLimit = InputParam("accepts a value from 1 Watt through the maximum reflected power.\n"
                                     "The maximum is also limited by negative cable attenuation factors settings\n",
                                     0, 2)  # TODO find out range

    # command 8
    PowerSetPoint = InputParam("set point level is in Watt or Volt depending on the regulation mode.\n"
                               "accepts 0 to maximum RF output power in Watt,\n"
                               "accepts 0 to maximum external feedback value in Volts.\n",
                               0, 2)

    # command 10
    RFOnTimeLimit = InputParam("accepts values from 0 to 3600s. A 0 deactivates this function",
                               0, 2, range(0, 3601))

    # command 14
    ActiveControlMode = InputParam("accepts values only these specific values \n"
                                   "2, Host Port\n"
                                   "4, User Port\n"
                                   "6, Front Panel\n"
                                   "10, Reset Front Panel display\n"
                                   "11, Disable front panel program menu presets\n"
                                   "12, disable all front panel functions except display soft key\n"
                                   "13, Diable all front panel functions\n"
                                   "20, Reset front panel display\n"
                                   "22, Set front panel display to show only ready, active, error\n"
                                   "23, Turn off front panel display\n",
                                   0, 1, (2, 4, 6, 10, 11, 12, 13, 20, 22, 23))

    # command 19
    NumberOfRecipeSteps = InputParam("accepts a value of 0 to 2",
                                     0, 1, range(0, 3))

    # command 21, 22, 23
    RecipeStepNumber = InputParam("accepts values from 1 to 2",
                                  0, 1, range(1, 3))
    RecipeRampRunTime = InputParam("accepts a value from 0 to 36000 (= one hour) in tenths of a second",
                                   1, 2, range(0, 36001))
    PowerStepSetPoint = InputParam("set point level is in Watt or Volt depending on the regulation mode.\n"
                                   "accepts 0 to maximum RF output power in Watt,\n"
                                   "accepts 0 to maximum external feedback value in Volts.\n",
                                   1, 2)

    # command 24, 25
    PresetsNumber = InputParam("accepts a value from 1 to 5",
                               0, 1, (1, 6))

    # command 29
    RemoteControlOverride = InputParam("accepts Bitwise enabling from int values 0 to 15.\n"
                                       " Please insert as an int!",
                                       0, 1, range(0, 15+1))

    # command 30
    UserPortScaling = InputParam("accepts values from 4 to 40.\n"
                                 "inserted value is divided by 2 internally to get 0.5 Volt steps (2 to 20)\n",
                                 0, 1, range(4, 41))

    # command 31, 32
    RampRiseFallTime = InputParam("accepts values from 0 t 2400 (=4 min) in tenths of a second",
                                  0, 2, range(0, 2401))

    # command 33
    SecondsToRFTurnOff = InputParam(" accepts values from 0 to 200s", 0, 1, range(0, 201))
    PowerLimitTriggerInW = InputParam("accepts a value 1 lesser than set by command 5 or RFoutputpower*reflected factor",
                                      1, 2)

    # command 69
    IgnoredByte = InputParam("", 0, 1)
    BaudRate = InputParam("accepts the baud rates: 9600, 19200,38400, 57600, 115200 (send 0 for this rate)",
                          1, 2, (0, 9600, 19200, 38400, 57600))

    # command 93
    PulsingFrequency = InputParam("accepts values from 1 Hz to the maximum pulsing frequency\n",
                                  0, 4)  # TODO find out range

    # command 96
    PulsingDutyCycle = InputParam("accepts a value in percent from 1 to 99",
                                  0, 2, range(1, 100))



class Parameter(object):
    # command 151
    CSR = 'CSR'

    RAMP_ON = 'Ramp on'
    RAMP_OFF = 'Ramp off'

    # command 152
    TIME_LIMIT_RF_TURN_OFF = "time limit until RF is turned off"
    POWER_LIMIT_TRIGGER = "Power limit trigger"

    # command 154
    FORWARD_POWER = 6
    LOAD_POWER = 7
    EXTERNAL_POWER = 8

    # command 155
    HOST_PORT = 2
    USER_PORT = 4
    FRONT_PANEL = 6

    # command 162
    # byte 0
    RECIPE_RUN_ACTIVE = (0, 2)
    OUTPUT_POWER = (0, 5)
    RF_ON_REQUESTED = (0, 6)
    SET_POINT_TOLERANCE = (0, 7)
    # byte 1
    END_OF_TARGET_LIFE = (1, 0)
    OVERTEMPERATURE_FAULT = (1, 3)
    INTERLOCK = (1, 7)
    # byte 2 and 3 reserved
    # byte 4
    DC_CURRENT_LIMIT_WARNING = (4, 0)
    PROFIBUS_ERROR = (4, 2)
    FAULT_PRESENT = (4, 5)
    CEX_IS_LOCKED = (4, 7)

    # command 164
    SET_POINT_VALUE = "set point value in W or V"
    # same output as 154 for byte 3

    # command 212
    AE_BUS_ADRESS = "AE_BUS adress always 1"
    BAUD_RATE = "Baud rate returns 0 for 115200"

    # command 223
    # byte 0
    INTERLOCK_LOOP_OPEN = (0, 0)
    SMPS_TEMP_TOO_HIGH = (0, 1)
    RF_GENERATOR_TEMPERATURE_TOO_HIGH = (0, 2)
    RF_POWER_SECTION_FAILURE = (0, 4)
    AD_CONVERSION_FAILURE = (0, 5)
    # byte 1
    EXTERNAL_PULSE_TOO_SHORT = (1, 1)
    RF_ON_TIME_EXCEEDED = (1, 2)
    SOFTWARE_ERROR = (1, 6)
    # byte 3 and 4 are unassigned
