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
from cesar136.parameter import AbstractParameter, StringParameter, RangeParameter
from cesar136.validator import ValidationError, NullValidator

class CesarDevice(object):
    MAXIMUM_POWER = 600


class Parameter(object):

    class CSRCode(RangeParameter):
        UNKNOWN = -1

        ACCEPTED = 0
        CONTROL_CODE_INCORRECT = 1
        OUTPUT_ON = 2
        DATA_OUT_OF_RANGE = 4
        ACTIVE_FAULT = 7
        DATA_BYTE_COUNT_INCORRECT = 9
        RECIPE_ACTIVE = 19
        FREQUENCY_OUT_OF_RANGE = 50
        DUTY_CYCLE_OUT_OF_RANGE = 51
        COMMAND_NOT_DETECTED = 53
        COMMAND_NOT_ACCEPTED = 99

        RANGE = [
            ACCEPTED, CONTROL_CODE_INCORRECT, OUTPUT_ON, DATA_OUT_OF_RANGE, ACTIVE_FAULT, DATA_BYTE_COUNT_INCORRECT,
            RECIPE_ACTIVE, FREQUENCY_OUT_OF_RANGE, DUTY_CYCLE_OUT_OF_RANGE, COMMAND_NOT_DETECTED, COMMAND_NOT_ACCEPTED,
        ]

        def __init__(self):
            super(Parameter.CSRCode, self).__init__(1)

        def parse(self, raw_data):
            if len(raw_data) > 0:
                return super(Parameter.CSRCode, self).parse(raw_data[0])
            raise ValidationError("Given CSRCode is empty")

    class Regulation(RangeParameter):
        FORWARD_POWER = 6
        LOAD_POWER = 7
        EXTERNAL = 8

        RANGE = [FORWARD_POWER, LOAD_POWER, EXTERNAL]

        def __init__(self):
            super(Parameter.Regulation, self).__init__(1)

    class Setpoint(RangeParameter):
        MAXIMUM = 0  # 0 corresponds to the max, for some reasons.. ask the device developers
        MINIMUM = 1
        RANGE = range(0, CesarDevice.MAXIMUM_POWER + 1)

        def __init__(self):
            super(Parameter.Setpoint, self).__init__(2)

    class ForwardPower(RangeParameter):
        MINIMUM = 30
        MAXIMUM = CesarDevice.MAXIMUM_POWER
        RANGE = range(MINIMUM, MAXIMUM + 1)

        def __init__(self):
            super(Parameter.ForwardPower, self).__init__(2)

    class ReflectedPower(AbstractParameter):
        def __init__(self):
            super(Parameter.ReflectedPower, self).__init__(2)

    class OnTimeLimit(RangeParameter):
        DISABLE = 0
        MINIMUM = 1
        MAXIMUM = 3600
        RANGE = range(0, MAXIMUM + 1)

        def __init__(self):
            super(Parameter.OnTimeLimit, self).__init__(2)

    class ControlMode(RangeParameter):
        SERIAL_CONTROL = 2
        ANALOG_CONTROL = 4
        LOCAL_CONTROL = 6
        LOCAL_CONTROL_OPERATIONAL_RESET = 10
        LOCAL_CONTROL_OPERATIONAL_DISABLE_MENU = 11
        LOCAL_CONTROL_OPERATIONAL_DISABLE_ALL_EXCEPT_DISPLAY = 12
        LOCAL_CONTROL_OPERATIONAL_DISABLE_ALL = 13
        LOCAL_CONTROL_DISPLAY_RESET = 20
        LOCAL_CONTROL_DISPLAY_RESTRICTED = 22
        LOCAL_CONTROL_DISPLAY_OFF = 23

        RANGE = [
            SERIAL_CONTROL, ANALOG_CONTROL, LOCAL_CONTROL, LOCAL_CONTROL_OPERATIONAL_RESET,
            LOCAL_CONTROL_OPERATIONAL_DISABLE_MENU, LOCAL_CONTROL_OPERATIONAL_DISABLE_ALL_EXCEPT_DISPLAY,
            LOCAL_CONTROL_OPERATIONAL_DISABLE_ALL, LOCAL_CONTROL_DISPLAY_RESET, LOCAL_CONTROL_DISPLAY_RESTRICTED,
            LOCAL_CONTROL_DISPLAY_OFF,
        ]

        def __init__(self):
            super(Parameter.ControlMode, self).__init__(1)

    class Recipe(object):
        """
                Warning: RecipesNumber != RecipeNumber
                RecipesNumber can be 0, whereas RecipeNumber can only be 1 or 2

                RecipesNumber is the number of recipes
                RecipeNumber is the number of a recipe
        """

        class NumberOf(RangeParameter):
            MINIMUM = 0
            MAXIMUM = 2
            RANGE = range(MINIMUM, MAXIMUM + 1)

            def __init__(self):
                super(Parameter.Recipe.NumberOf, self).__init__(1)

        class Number(RangeParameter):
            MINIMUM = 1
            MAXIMUM = 2
            RANGE = range(MINIMUM, MAXIMUM + 1)

            def __init__(self):
                super(Parameter.Recipe.Number, self).__init__(1)

        class RampTime(RangeParameter):
            MINIMUM = 0
            MAXIMUM = 36000  # in 1/10 sec
            RANGE = range(MINIMUM, MAXIMUM + 1)

            def __init__(self):
                super(Parameter.Recipe.RampTime, self).__init__(2)

        class Setpoint(RangeParameter):
            MINIMUM = 1
            MAXIMUM = 0
            RANGE = range(MINIMUM, CesarDevice.MAXIMUM_POWER + 1)

            def __init__(self):
                super(Parameter.Recipe.Setpoint, self).__init__(1)

        class RunTime(RangeParameter):
            MINIMUM = 0
            MAXIMUM = 36000  # in 1/10 sec
            RANGE = range(MINIMUM, MAXIMUM + 1)

            def __init__(self):
                super(Parameter.Recipe.RunTime, self).__init__(2)

    class Preset(RangeParameter):
        MINIMUM = 1
        MAXIMUM = 5
        RANGE = range(MINIMUM, MAXIMUM + 1)

        def __init__(self):
            super(Parameter.Recipe.Preset, self).__init__(1)

    # TODO: Test whether it's lsb of msb ...
    # e.g. for BIT_ENABLE_ON_OFF_BUTTON is Bit 0:
    # lsb -> 0b10000000
    # msb -> 0b00000001
    #
    # and luckily there is no readback function for it available... yay
    class ControlOverride(RangeParameter):
        MINIMUM = 0
        MAXIMUM = 31  # 2^5 - 1 (since we have 5 bits to control)
        RANGE = range(MINIMUM, MAXIMUM + 1)

        BIT_ENABLE_ON_OFF_BUTTON = 1
        BIT_ENABLE_ROTATING_KNOB = 2
        BIT_ENABLE_MATCHING_KEYS = 4
        BIT_ENABLE_SETTING_ON_OFF_USER_PORT = 8
        BIT_ENABLE_SERRING_POWER_SETPOINT_USER_PORT = 16

        def __init__(self):
            super(Parameter.ControlOverride, self).__init__(1)

    class VoltageScaling(RangeParameter):
        """
            physically: 2V to 20V
            logically: 4 Units to 40 Units
            Hence we get a 0.5V granualarity. E.g. 12V <- 24 Units
        """
        MINIMUM = 4
        MAXIMUM = 40
        RANGE = range(MINIMUM, MAXIMUM + 1)

        def __init__(self):
            super(Parameter.VoltageScaling, self).__init__(1)

    class RampTime(RangeParameter):
        """
            in 1/10 sec
        """
        DISABLED = 0
        MINIMUM = 1
        MAXIMUM = 2400
        RANGE = (0, MAXIMUM + 1)

        KEY_RAMP_UP = 1
        KEY_RAMP_DOWN = 2

        def __init__(self):
            super(Parameter.RampTime, self).__init__(2)

    class ReflectedPowerParameter(object):
        class TimeLimit(RangeParameter):
            """
                in seconds
            """
            DISABLED = 0
            MINIMUM = 1
            MAXIMUM = 200
            RANGE = range(0, MAXIMUM)

            def __init__(self):
                super(Parameter.ReflectedPowerParameter.TimeLimit, self).__init__(1)

        class PowerTrigger(RangeParameter):
            """
                in Watt
            """
            DISABLED = 0
            MINIMUM = 1
            MAXIMUM = CesarDevice.MAXIMUM_POWER
            RANGE = (0, MAXIMUM + 1)

            def __init__(self):
                super(Parameter.ReflectedPowerParameter.PowerTrigger, self).__init__(2)

    # TODO: Check how to generate and parse the raw data, first byte is ignored, but dont know
    # how they are ordered
    class BaudRate(RangeParameter):
        RATE_9600 = 9600
        RATE_19200 = 19200
        RATE_38400 = 38400
        RATE_57600 = 57600
        RATE_115200 = 0

        RANGE = [RATE_9600, RATE_19200, RATE_38400, RATE_57600, RATE_115200]

        def __init__(self):
            super(Parameter.BaudRate, self).__init__(2)

    class IgnoredByte(AbstractParameter):
        def __init__(self):
            super(Parameter.IgnoredByte, self).__init__(1)

    class PulsingFrequency(RangeParameter):
        MINIMUM = 1
        MAXIMUM = 2000  # TODO: wrong max
        RANGE = range(MINIMUM, MAXIMUM + 1)

        def __init__(self):
            super(Parameter.PulsingFrequency, self).__init__(4)

    class PulsingDutyCycle(RangeParameter):
        MINIMUM = 1
        MAXIMUM = 100
        RANGE = range(MINIMUM, MAXIMUM + 1)

        def __init__(self):
            super(Parameter.PulsingDutyCycle, self).__init__(2)

    class SupplyType(StringParameter):
        def __init__(self):
            super(Parameter.SupplyType, self).__init__(5, NullValidator())

    class ModelNumber(StringParameter):
        def __init__(self):
            super(Parameter.ModelNumber, self).__init__(5, NullValidator())

    class Status(AbstractParameter):
        BIT_RECIPE_ACTIVE = (0, 2)
        BIT_OUTPUT_POWER = (0, 5)
        BIT_RF_ON_REQUESTED = (0, 6)
        BIT_SETPOINT_TOLERANCE = (0, 7)
        BIT_END_OF_TARGET_LIFE = (1, 0)
        BIT_OVERTEMPERATURE_FAULT = (1, 3)
        BIT_INTERLOCK = (1, 7)
        BIT_DC_CURRENT_LIMIT_WARNING = (3, 0)
        BIT_PROFIBUS_ERROR = (3, 2)
        BIT_FAULT_PRESENT = (3, 5)
        BIT_CEX_IS_LOCKED = (3, 7)

        def __init__(self):
            super(Parameter.Status, self).__init__(4, NullValidator())

    class Runtime(AbstractParameter):
        def __init__(self):
            super(Parameter.Runtime, self).__init__(4, NullValidator())

    class BusAddress(AbstractParameter):
        def __init__(self):
            super(Parameter.BusAddress, self).__init__(1, NullValidator())

    class FaultRegister(AbstractParameter):
        BIT_INTERLOCK_OPEN = (0, 0)
        BIT_SMPS_TEMPERATURE_TOO_HIGH = (0, 1)
        BIT_RF_GENERATOR_TEMPERATURE_TOO_HIGH = (0, 2)
        BIT_RF_POWER_FAILURE = (0, 4)
        BIT_AD_CONVERSION_FAILURE = (0, 5)
        BIT_EXTERNAL_PULSE_TOO_SHORT = (1, 1)
        BT_RF_TIME_EXCEEDED = (1, 2)
        BIT_SOFTWARE_ERROR = (1, 6)

        def __init__(self):
            super(Parameter.FaultRegister, self).__init__(4, NullValidator())
