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


from cesar136.raw_message_packet import MessagePacket
from cesar136.data_structure import Response


class ReceivedByteArray(MessagePacket):

    def __init__(self, binary_data):
        super(ReceivedByteArray, self).__init__(binary_data)

    def checkForCompletness(self):
        # returns the xor value for the complete received package
        # using compute_checksum() to append checksum to _intArray
        # any return other than zero indicates an incomplete message
        self.compute_checksum()
        return self.xor(self._intArray)

    def extractData(self, DataConfig):
        self._formatedData = Response()
        index = 0

        for config in DataConfig:
            end_Of_Data = index + config._numberOfBytes
            tempData = self._data[index:end_Of_Data]
            config.analyze(tempData)
            self._formatedData.set_parameter(config)
            index = end_Of_Data

        return self._formatedData

    def getCesarAddress(self):
        return self._address

    def getCommandId(self):
        return self._command_id
