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

#command 2
def Output_On():
    return interactionProcess(presetCommands.turnOutputOn)

#command 3
def set_regulation_mode(data):
    return interactionProcess(presetCommands.setRegulationMode, data)

#command 4
def set_forward_power_lim(data):
    return interactionProcess(presetCommands.setForwardPowerLimit, data)

#command 5
def set_reflected_power_lim(data):
    return interactionProcess(presetCommands.setReflectedPowerLimit, data)

#command 8
def set_power_setpoint(data):
    return interactionProcess(presetCommands.setPowerSetPoint, data)

#command 10
def set_RF_on_time_limit(data):
    return interactionProcess(presetCommands.setRFOnTimeLimit, data)

#command 14
def set_active_control_mode(data):
    return interactionProcess(presetCommands.setActiveControlMode, data)

#command 19
def set_number_of_recipe_steps(data):
    return interactionProcess(presetCommands.setNumberOfRecipeSteps, data)

# command 21
def set_recipe_step_ramp_time(data):
    return interactionProcess(presetCommands.setRecipeStepRampTime, data)

# command 22
def set_step_set_point(data):
    return interactionProcess(presetCommands.setStepSetPoint, data)

# command 23
def set_recipe_step_run_time(data):
    return interactionProcess(presetCommands.setRecipeStepRunTime, data)

# command 24
def save_presets(data):
    return interactionProcess(presetCommands.savePresets, data)

# command 25
def restore_presets(data):
    return interactionProcess(presetCommands.restorePresets, data)

# command 29
def set_remote_control_override(data):
    return interactionProcess(presetCommands.setRemoteControlOverride, data)

# command 30
def set_user_port_scaling(data):
    return interactionProcess(presetCommands.setUserPortScaling, data)

# command 31
def set_RF_ramping_rise_time(data):
    return interactionProcess(presetCommands.setRFOnOffRampingRiseTime, data)

# command 32
def set_RF_ramping_fall_time(data):
    return interactionProcess(presetCommands.setRFOnOffRampingFallTime, data)

# command 33
def set_reflect_pow_params(data):
    return interactionProcess(presetCommands.setReflectedPowerParameters,data)

# command 69
def set_baud_rate(data):
    return interactionProcess(presetCommands.setSerialBaudRate, [0].append(data))

# command 93
def set_pulsing_frequency(data):
    return interactionProcess(presetCommands.setPulsingFrequency, data)

# command 96
def set_pulsing_duty_cyle(data):
    return interactionProcess(presetCommands.reportPulsingDutyCycle, data)

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
def get_recipe_step_ramp_time(data):
    return interactionProcess(presetCommands.reportRecipeStepRampTime, data)


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
