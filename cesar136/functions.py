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

# data has to be in form of a list even when it is only one parameter
# the data for each parameter has to be in correct order like it is listed where
# the command is set (command.py)


from cesar136.com_protocol import interactionProcess
from cesar136.command import *


# command 1
def Output_Off():
    return interactionProcess(presetCommands.turnOutputOff)


# command 2
def Output_On():
    return interactionProcess(presetCommands.turnOutputOn)


# command 3
def set_regulation_mode(regulationMode):
    return interactionProcess(presetCommands.setRegulationMode, [regulationMode])


# command 4
def set_forward_power_lim(forward_power_limit):
    return interactionProcess(presetCommands.setForwardPowerLimit, [forward_power_limit])


# command 5
def set_reflected_power_lim(reflected_power_limit):
    return interactionProcess(presetCommands.setReflectedPowerLimit, [reflected_power_limit])


# command 8
def set_power_setpoint(power_set_point):
    return interactionProcess(presetCommands.setPowerSetPoint, [power_set_point])


# command 10
def set_RF_on_time_limit(on_time_limit):
    return interactionProcess(presetCommands.setRFOnTimeLimit, [on_time_limit])


# command 14
def set_active_control_mode(active_control_mode):
    return interactionProcess(presetCommands.setActiveControlMode, [active_control_mode])


# command 19
def set_number_of_recipe_steps(number_of_recipe_steps):
    return interactionProcess(presetCommands.setNumberOfRecipeSteps, [number_of_recipe_steps])


# command 21
def set_recipe_step_ramp_time(step_number, ramp_time):
    return interactionProcess(presetCommands.setRecipeStepRampTime, [step_number, ramp_time])


# command 22
def set_step_set_point(step_number, set_point):
    return interactionProcess(presetCommands.setStepSetPoint, [step_number, set_point])


# command 23
def set_recipe_step_run_time(step_number, run_time):
    return interactionProcess(presetCommands.setRecipeStepRunTime, [step_number, run_time])


# command 24
def save_presets(preset_number):
    return interactionProcess(presetCommands.savePresets, [preset_number])


# command 25
def restore_presets(preset_number):
    return interactionProcess(presetCommands.restorePresets, [preset_number])


# command 29
def set_remote_control_override(int_from_bits):
    return interactionProcess(presetCommands.setRemoteControlOverride, [int_from_bits])


# command 30
def set_user_port_scaling(user_port_scaling):
    return interactionProcess(presetCommands.setUserPortScaling, [user_port_scaling])


# command 31
def set_RF_ramping_rise_time(RFramping_rise_time):
    return interactionProcess(presetCommands.setRFOnOffRampingRiseTime, [RFramping_rise_time])


# command 32
def set_RF_ramping_fall_time(RFramping_fall_time):
    return interactionProcess(presetCommands.setRFOnOffRampingFallTime, [RFramping_fall_time])


# command 33
def set_reflect_pow_params(seconds_until_RF_turned_off, power_limit_trigger):
    return interactionProcess(presetCommands.setReflectedPowerParameters, [seconds_until_RF_turned_off,
                                                                           power_limit_trigger])


# command 69
def set_baud_rate(baud_rate):
    # first byte is ignored
    return interactionProcess(presetCommands.setSerialBaudRate, [1,baud_rate])


# command 93
def set_pulsing_frequency(pulsing_frequency):
    return interactionProcess(presetCommands.setPulsingFrequency, [pulsing_frequency])


# command 96
def set_pulsing_duty_cyle(pulsing_duty_cycle):
    return interactionProcess(presetCommands.reportPulsingDutyCycle, [pulsing_duty_cycle])


# command 128
def get_power_supply_type():
    return interactionProcess(presetCommands.reportPowerSupplyType)


# command 129
def get_model_number():
    return interactionProcess(presetCommands.reportModelNumber)


# command  151
def get_RF_ramp_OnOff_parameters():
    return interactionProcess(presetCommands.reportRFRampOnOff)


# command 152
def get_reflected_power_parameter():
    return interactionProcess(presetCommands.reportReflectedPowerParameters)


# command 154
def get_regulation_mode():
    return interactionProcess(presetCommands.reportRegulationMode)


# command 155
def get_active_control_mode():
    return interactionProcess(presetCommands.reportActiveControlMode)


# command 162
def get_process_status():
    return interactionProcess(presetCommands.reportProcessStatus)


# command 164
def get_set_point_and_regulation_mode():
    return interactionProcess(presetCommands.reportSetPointAndRegulationMode)


# command 165
def get_forward_power():
    return interactionProcess(presetCommands.reportForwardPower)


# command 166
def get_reflected_power():
    return interactionProcess(presetCommands.reportReflectedPower)


# command 167
def get_delivered_power():
    return interactionProcess(presetCommands.reportDeliveredPower)


# command 169
def get_forward_power_limit():
    return interactionProcess(presetCommands.reportForwardPowerLimit)


# command 170
def get_reflected_power_limit():
    return interactionProcess(presetCommands.reportReflectedPowerLimit)


# command 191
def get_recipe_step_ramp_time(recipe_step_number):
    return interactionProcess(presetCommands.reportRecipeStepRampTime, recipe_step_number)


# command 193
def get_pulsing_frequency():
    return interactionProcess(presetCommands.reportPulsingFrequency)


# command 196
def get_pulsing_duty_cycle():
    return interactionProcess(presetCommands.reportPulsingDutyCycle)


# command 205
def get_unit_run_time():
    return interactionProcess(presetCommands.reportUnitRunTime)


# command 212
def get_baud_rate():
    return interactionProcess(presetCommands.reportSerialPortAddressAndBaudRate)


# command 223
def get_fault_status_register():
    return interactionProcess(presetCommands.reportFaultStatusRegister)


# command 243
def get_RF_on_time_limit():
    return interactionProcess(presetCommands.reportRFOnTimeLimit)
