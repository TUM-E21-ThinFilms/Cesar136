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


from cesar136.cesar import get_transport
from cesar136.CeasarCommunication import *
from cesar136.command import *

ser = get_transport()
CSRCodes = {0: "Command accepted",
            1: "Control code is incorrect",
            2: "Output is on (change not allowed)",
            4: "Data is out of range",
            7: "Active fault(s) exist",
            9: "Data byte count is incorrect",
            19: "Recipe is active (change not allowed)",
            50: "The frequency is out of range",
            51: "The duty cycle is out of range",
            53: "The device controlled by the command is not detected",
            99: "Command not accepted (there is no such command)"}


def interactionProcess(Command):
    Command.prepareInteraction()
    ser.write(bytearray(Command._intArray))
    response = ReceivedByteArray(bytearray(ser.read(10))[1::])
    if response.checkForCompletness() != 0:
        raise RuntimeError("Computer received no valid response, try again.")
    else:
        if Command.CSRonly:
            if response._lenData == 1:
                answer = CSRCodes[response._data]
            else:
                raise ValueError("Something must be wrong, CSR contained more data")
        else:
            response.extractData(Command.DataConfig)
            answer = response.formatedData
    return answer


def Output_Off():
    print(interactionProcess(turnOutputOff))


def getModelNumber():
    print(interactionProcess(reportModelNumber))


def getPowerSupplyType():
    print(interactionProcess(reportPowerSupplyType))


def getRFRampOnOff():
    print(interactionProcess(reportRFRampOnOff))
