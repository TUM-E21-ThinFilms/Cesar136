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

from cesar136.command import Command
from cesar136.raw_message_packet import MessagePacket
from cesar136.data_structure import Response

from e21_util.serial_connection import AbstractTransport, SerialTimeoutException
from e21_util.interface import Loggable
from e21_util.lock import InterProcessTransportLock
from e21_util.error import CommunicationError


class Protocol(Loggable):
    RESPONSE_MAX_LENGTH = 10

    def __init__(self, transport: AbstractTransport, logger):
        super(Protocol, self).__init__(logger)
        assert isinstance(transport, AbstractTransport)

        self._transport = transport

    def clear(self):
        with InterProcessTransportLock(transport):
            self.logger.debug("Clearing message queue")
            while True:
                try:
                    self._transport.read_bytes(32)
                except SerialTimeoutException:
                    return

    def execute(self, command: Command):
        with InterProcessTransportLock(self._transport):
            self._write(command)

            return self._read_response()

    def _write(self, command: Command):
        data = command.get_raw()
        self._logger.debug("Sending message '%s'", " ".join(map(hex, data)))

        self._transport.write(data)

    def _read_response(self, command: Command):

        try:
            # in fact, we can compute how long the response will be, based on the first two bytes read
            # but this works for us and we dont care about more details...
            raw_response = self._transport.read(self.RESPONSE_MAX_LENGTH)
        except SerialTimeoutException:
            raise CommunicationError("Could not read response. Timeout")

        # Remove the first data element, since this contains no information
        # in fact, we dont know why we get this data since its not part of the documentation
        raw_response = raw_response[1:]

        msg = MessagePacket.from_raw(raw_response)

        if not msg.is_valid():
            raise CommunicationError("Received response is not valid")

        response = Response(command.get_data_config())

        # we received not the same amount of data than expected. This occurs only in two cases:
        # 1. The protocol was not correctly specified by the user
        # 2. The device returns just an CSR code instead of the data
        if command.get_expected_response_data_length() != msg.get_data_length():
            # This is then the case 2
            if msg.get_data_length() == 1:
                response.get_csr().set_data(msg.get_data()[0])
            else:
                raise CommunicationError(
                    "Received an unexpected amount of data (%s bytes) from device. Expectation was %s bytes (excluding CSR)".format(
                        msg.get_data_length, command.get_expected_response_data_length()))
        else:
            # Here we just assign the data to the correct parameter

            data_start = 0
            raw_data = msg.get_data()

            for config in command.get_data_config():
                data_end = index + config.get_length()
                config.set_data(raw_data[data_start:data_end])
                data_start = data_end

        return response