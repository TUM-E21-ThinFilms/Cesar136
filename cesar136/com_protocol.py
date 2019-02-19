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
from cesar136.received_message_packet import ReceivedByteArray
from cesar136.command import Command
from cesar136.data_structure import CSRCodes

ser = get_transport()


def interactionProcess(command: Command, data=None):
    if data:
        command.set_data(data)
    command.prepareInteraction()
    ser.write(bytearray(command._intArray))
    # no valuable information in first byte
    # just reading 10 bytes because the unit is not usually sending more than that
    raw_response = ReceivedByteArray(bytearray(ser.read(10))[1::])
    if raw_response.checkForCompletness() != 0:
        raise ValueError("Computer received no valid response, try again.")
    else:
        probableCSR = raw_response._data_length != command._DataBytesExpected
        if command._CSRonly or probableCSR:
            if raw_response._data_length == 1:
                # _data is list with one element
                answer = CSRCodes[raw_response._data[0]]
            else:
                # Should not happen. Either message is wrong or we just get a CSR
                # if we have more than one data byte returned then probably the protocol is wrong
                raise ValueError("Something must be wrong, CSR contained more data. Probably the protocol is wrong")
        else:
            answer = raw_response.extractData(command._DataConfig)
    return answer

# response = get_power_supply_type()
# response.get_parameter(Parameter.RAMP_OFF).get()
# response.get_parameter(Parameter.DEINE_MUTTER).get()
