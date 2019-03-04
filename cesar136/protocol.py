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

from typing import List

from e21_util.serial_connection import AbstractTransport, SerialTimeoutException
from e21_util.interface import Loggable
from e21_util.error import CommunicationError

from cesar136.command import Command
from cesar136.message import MessagePacket
from cesar136.io_data import Output
from cesar136.response import Response


class Protocol(Loggable):
    RESPONSE_MAX_LENGTH = 10
    ACK = 0x06
    NAK = 0x15

    def __init__(self, transport: AbstractTransport, logger):
        super(Protocol, self).__init__(logger)
        assert isinstance(transport, AbstractTransport)

        self._transport = transport

    def clear(self):
        with self._transport:
            self._logger.debug("Clearing message queue")
            while True:
                try:
                    self._transport.read_bytes(32)
                except SerialTimeoutException:
                    return

    def execute(self, command: Command):
        with self._transport:
            self._write(command)

            return self._read_response(command)

    def _write(self, command: Command):
        data = command.get_raw()
        self._logger.debug("Sending message '%s'", " ".join(map(hex, data)))

        self._transport.write(data)

    def _read_response(self, command: Command):

        try:
            # Read exactly one byte. This is the verification of the cesar unit
            # its either ACK (0x06) or NACK (0x15)
            verification = self._transport.read(1)

            if verification == self.ACK:
                pass
            elif verification == self.NAK:
                raise CommunicationError("Device returned NAK")

            # in fact, we can compute how long the response will be, based on the first two bytes read
            # but this works for us and we dont care about more details...
            raw_response = self._transport.read(self.RESPONSE_MAX_LENGTH)

            # Now send back a ACK since we got our data, even if the data is not valid
            # We just dont care about this. If the data is not valid, we throw an execption
            # and the calling api will re-engage into sending the message
            self._transport.write(bytearray(self.ACK))
        except SerialTimeoutException:
            raise CommunicationError("Could not read response. Timeout")

        raw_response = bytearray(raw_response)

        msg = MessagePacket.from_raw(raw_response)

        if not msg.is_valid():
            raise CommunicationError("Received response is not valid")

        response = Response(command.get_outputs())

        # we received not the same amount of data than expected. This occurs only in two cases:
        # 1. The protocol was not correctly specified by the user
        # 2. The device returns just an CSR code instead of the data
        if command.get_expected_response_data_length() != msg.get_data_length():
            # This is then the case 2
            if msg.get_data_length() == 1:
                response.get_csr().set_raw(msg.get_data())
            else:
                raise CommunicationError(
                    "Received an unexpected amount of data (%s bytes) from device. Expectation was %s bytes (excluding CSR)".format(
                        msg.get_data_length, command.get_expected_response_data_length()))
        else:
            # Here we just assign the data to the correct output
            self._assign_data(msg.get_data(), command.get_outputs())

        return response

    def _assign_data(self, raw_data, outputs: List[Output]):
        data_start = 0

        for output in outputs:
            data_end = data_start + output.get_length()
            output.set_raw(raw_data[data_start:data_end])
            data_start = data_end
