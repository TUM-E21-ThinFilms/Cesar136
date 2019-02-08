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

from cesar136.com_protocol import interactionProcess
from cesar136.command import *


# command 1
def Output_Off():
    return interactionProcess(turnOutputOff)


# command 33
def set_reflect_pow_params(data):
    return interactionProcess(setReflectedPowerParameters,data)





# command 128
def get_power_supply_type():
    return interactionProcess(reportPowerSupplyType)


# command 129
def get_model_number():
    return interactionProcess(reportModelNumber)


# command  151
def get_RF_ramp_OnOff_parameters():
    return interactionProcess(reportRFRampOnOff)


# command 152
def get_reflected_power_parameter():
    return interactionProcess(reportReflectedPowerParameters)


# command 154
def get_regulation_mode():
    return interactionProcess(reportRegulationMode)


# command 155
def get_active_control_mode():
    return interactionProcess(reportActiveControlMode)


# command 162
def get_process_status():
    return interactionProcess(reportProcessStatus)


# command 164
def get_set_point_and_regulation_mode():
    return interactionProcess((reportSetPointAndRegulationMode))


# command 165
def get_forward_power():
    return interactionProcess(reportForwardPower)


# command 166
def get_reflected_power():
    return interactionProcess(reportReflectedPower)


# command 167
def get_delivered_power():
    return interactionProcess(reportDeliveredPower)


# command 169
def get_forward_power_limit():
    return interactionProcess(reportForwardPowerLimit)


# command 170
def get_reflected_power_limit():
    return interactionProcess(reportReflectedPowerLimit)


# command 191
def get_recipe_step_ramp_time(data):
    return interactionProcess(reportRecipeStepRampTime, data)


# command 193
def get_pulsing_frequency():
    return interactionProcess(reportPulsingFrequency)


# command 196
def get_pulsing_duty_cycle():
    return interactionProcess(reportPulsingDutyCycle)


# command 205
def get_unit_run_time():
    return interactionProcess(reportUnitRunTime)


# command 212
def get_baud_rate():
    return interactionProcess(reportSerialPortAddressAndBaudRate)


# command 223
def get_fault_status_register():
    return interactionProcess(reportFaultStatusRegister)


# command 243
def get_RF_on_time_limit():
    return interactionProcess(reportRFOnTimeLimit)
