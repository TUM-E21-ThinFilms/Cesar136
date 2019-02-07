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

def Output_Off():
    return interactionProcess(turnOutputOff)


def get_model_number():
    return interactionProcess(reportModelNumber)


def get_power_supply_type():
    return interactionProcess(reportPowerSupplyType)


def get_RF_ramp_OnOff():
    return interactionProcess(reportRFRampOnOff)


def get_reflected_power_parameter():
    return interactionProcess(reportReflectedPowerParameters)


def get_regulation_mode():
    return interactionProcess(reportRegulationMode)


def get_active_control_mode():
    return interactionProcess(reportActiveControlMode)

def get_process_status():
    return  interactionProcess(reportProcessStatus)

def get_set_point_and_regulation_mode():
    return interactionProcess((reportSetPointAndRegulationMode))

def get_forward_power():
    return interactionProcess(reportForwardPower)

def get_reflected_power():
    return interactionProcess(reportReflectedPower)

def get_delivered_power():
    return interactionProcess(reportDeliveredPower)

def get_forward_power_limit():
    return interactionProcess(reportForwardPowerLimit)

def get_reflected_power_limit():
    return  interactionProcess(reportReflectedPowerLimit)


def get_recipe_step_ramp_time(data):
    return interactionProcess(reportRecipeStepRampTime, data)

def get_pulsing_frequency():
    return interactionProcess(reportPulsingFrequency)

def get_pulsing_duty_cycle():
    return interactionProcess(reportPulsingDutyCycle)

def get_unit_run_time():
    return interactionProcess(reportUnitRunTime)

def get_baud_rate():
    return  interactionProcess(reportSerialPortAddressAndBaudRate)

def get_fault_status_register():
    return  interactionProcess(reportFaultStatusRegister)

def get_RF_on_time_limit():
    return  interactionProcess(reportRFOnTimeLimit)


