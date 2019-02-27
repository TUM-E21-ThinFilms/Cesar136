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

from cesar136.constants import Parameter
from cesar136.protocol import Protocol
from cesar136.command import Command
from cesar136.io_data import Output, FlagOutput


class Driver(Loggable):
    def __init__(self, protocol, logger):
        super(Driver, self).__init__(logger)
        assert isinstance(protocol, Protocol)
        self._protocol = protocol

    def turn_off(self):
        return self._protocol.execute(Command(1, [], []))

    def turn_on(self):
        return self._protocol.execute(Command(2, [], []))

    def set_regulation_mode(self, mode):
        mode_input = Input(mode, Parameter.Regulation())
        return self._protocol.execute(Command(3, [mode_input], []))

    def set_forward_power_limit(self, power_limit):
        power_input = Input(power_limit, Parameter.ForwardPower())
        return self._protocol.execute(Command(4, [power_input], []))

    def set_reflected_power_limit(self, power_limit):
        power_input = Input(power_limit, Parameter.ReflectedPower())
        return self._protocol.execute(Command(5, [power_input], []))

    def set_setpoint(self, power_or_voltage):
        power_input = Input(power_or_voltage, Parameter.Setpoint())
        return self._protocol.execute(Command(8, [power_input], []))

    def set_time_limit(self, time_limit):
        time_input = Input(time_limit, Parameter.OnTimeLimit())
        return self._protocol.execute(Command(10, [time_input], []))

    def set_control_mode(self, control_mode):
        control_input = Input(control_mode, Parameter.ControlMode())
        return self._protocol.execute(Command(14, [control_input], []))

    def set_recipe_number(self, number):
        number_input = Input(number, Parameter.Recipe.NumberOf())
        return self._protocol.execute(Command(19, [number_input], []))

    def set_recipe_ramp_time(self, recipe_number, time):
        number_input = Input(recipe_number, Parameter.Recipe.Number())
        time_input = Input(time, Parameter.Recipe.RampTime())
        return self._protocol.execute(21, [number_input, time_input], [])

    def set_recipe_power(self, recipe_number, power):
        number_input = Input(recipe_number, Parameter.Recipe.Number())
        power_input = Input(power, Parameter.Recipe.Setpoint())
        return self._protocol.execute(22, [number_input, power_input], [])

    def set_recipe_run_time(self, recipe_number, time):
        number_input = Input(recipe_number, Parameter.Recipe.Number())
        time_input = Input(time, Parameter.Recipe.RunTime())
        return self._protocol.execute(23, [number_input, time_input], [])

    def save(self, preset_number):
        preset_input = Input(preset_number, Parameter.Preset())
        return self._protocol.execute(Command(24, [preset_input], []))

    def restore(self, preset_number):
        preset_input = Input(preset_number, Parameter.Preset())
        return self._protocol.execute(Command(25, [preset_input], []))

    def set_remote_control(self, control_mode):
        control_input = Input(control_mode, Parameter.ControlOverride())
        return self._protocol.execute(Command(29, [control_input], []))

    def set_user_port_scaling(self, voltage_scaling):
        voltage_input = Input(voltage_scaling, Parameter.VoltageScaling())
        return self._protocol.execute(Command(30, [voltage_input], []))

    def set_ramping_rise_time(self, time):
        time_input = Input(time, Parameter.RampTime())
        return self._protocol.execute(Command(31, [time_input], []))

    def set_ramping_fall_time(self, time):
        time_input = Input(time, Parameter.RampTime())
        return self._protocol.execute(Command(32, [time_input], []))

    def set_reflected_power_parameters(self, turn_off_time, power_limit_trigger):
        time_input = Input(turn_off_time, Parameter.ReflectedPowerParameter.TimeLimit())
        power_input = Input(power_limit_trigger, Parameter.ReflectedPowerParameter.PowerTrigger())
        return self._protocol.execute(Command(33, [time_input, power_input], []))

    def set_serial_baud_rate(self, baudrate):
        baudrate_input = Input(baudrate, Parameter.BaudRate())
        return self._protocol.execute(Command(69, [Input(0, Parameter.IgnoredByte()), baudrate_input], []))

    def set_pulsing_frequency(self, frequency):
        frequency_input = Input(frequency, Parameter.PulsingFrequency())
        return self._protocol.execute(Command(93, [frequency_input], []))

    def set_pulsing_duty_cycle(self, duty_cycle):
        cycle_input = Input(duty_cycle, Parameter.PulsingDutyCycle())
        return self._protocol.execute(Command(96, [cycle_input], []))

    def get_power_supply_type(self):
        return self._protocol.execute(Command(128, [], [Output(Parameter.SupplyType())]))

    def get_model_number(self):
        return self._protocol.execute(Command(129, [], [Output(Parameter.ModelNumber())]))

    def get_ramping_time(self):
        return self._protocol.execute(Command(151, [], [Output(Parameter.RampTime(), Parameter.RampTime.KEY_RAMP_UP),
                                                        Output(Parameter.RampTime(),
                                                               Parameter.RampTime.KEY_RAMP_DOWN)]))

    def get_reflected_power_parameters(self):
        return self._protocol.execute(Command(152, [], [Output(Parameter.ReflectedPowerParameter.TimeLimit()),
                                                        Output(Parameter.ReflectedPowerParameter.PowerTrigger())]))

    def get_regulation_mode(self):
        return self._protocol.execute(Command(154, [], [Output(Parameter.Regulation())]))

    def get_control_mode(self):
        return self._protocol.execute(Command(155, [], [Output(Parameter.ControlMode())]))

    def get_status(self):
        return self._protocol.execute(Command(162, [], [FlagOutput(Parameter.Status())]))

    def get_setpoint(self):
        return self._protocol.execute(Command(164, [], [Output(Parameter.Setpoint(), Output(Parameter.Regulation()))]))

    def get_forward_power(self):
        return self._protocol.execute(Command(165, [], [Output(Parameter.ForwardPower())]))

    def get_reflected_power(self):
        return self._protocol.execute(Command(166, [], [Output(Parameter.ReflectedPower())]))

    def get_delivered_power(self):
        return self._protocol.execute(Command(167, [], [Output(Parameter.ReflectedPower())]))

    def get_forward_power_limit(self):
        return self._protocol.execute(Command(169, [], [Output(Parameter.ForwardPower())]))

    def get_reflected_power_limit(self):
        return self._protocol.execute(Command(170, [], [Output(Parameter.ReflectedPower())]))

    def get_recipe_setpoint_and_time(self, recipe_number):
        number_input = Input(recipe_number, Parameter.Recipe.Number())
        return self._protocol.execute(Command(188, [number_input], [Output(Parameter.Recipe.Setpoint()),
                                                                    Output(Parameter.Recipe.RunTime())]))

    def get_recipe_ramp_time(self, recipe_number):
        number_input = Input(recipe_number, Parameter.Recipe.Number())
        return self._protocol.execute(Command(191, [number_input], [Output(Parameter.Recipe.RampTime())]))

    def get_pulsing_frequency(self):
        return self._protocol.execute(Command(193, [], [Output(Parameter.PulsingFrequency())]))

    def get_pulsing_duty_cycle(self):
        return self._protocol.execute(Command(196, [], [Output(Parameter.PulsingDutyCycle())]))

    def get_runtime(self):
        return self._protocol.execute(Command(205, [], [Output(Parameter.Runtime())]))

    def get_serial_address_and_baudrate(self):
        return self._protocol.execute(Command(212, [], [Output(Parameter.BusAddress()),
                                                        Output(Parameter.BaudRate())]))

    def get_fault_register(self):
        return self._protocol.execute(Command(223, [], [FlagOutput(Parameter.FaultRegister())]))

    def get_time_limit(self):
        return self._protocol.execute(Command(243, [], [Output(Parameter.OnTimeLimit())]))
