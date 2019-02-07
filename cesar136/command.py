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
from cesar136.CodesnBitFlags import *
from cesar136.data_structure import *


class Command():
    def __init__(self, commandNumber, DataBytesTosend, DatabytesExpected, DataConfig=None):
        self._commandNumber = commandNumber
        self._DataBytesToSend = DataBytesTosend
        self._DataBytesExpected = DatabytesExpected
        if self._commandNumber < 128:
            self._CSRonly = True
        else:
            self._CSRonly = False
            self._DataConfig = DataConfig

    def set_data(self, data):
        self._data = data

    def prepareInteraction(self):
        if self._DataBytesToSend != 0:
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber,
                                                                 self._DataBytesToSend,
                                                                 self._data)
        else:
            self._intArray = MessagePacket().createMessagePacket(self._commandNumber,
                                                                 self._DataBytesToSend)


turnOutputOff = Command(1, 0, 1)

reportPowerSupplyType = Command(128, 0, 5, [StringData(5)])
reportModelNumber = Command(129, 0, 5, [StringData(5)])
reportRFRampOnOff = Command(151, 0, 4, [IntegerData(2, Parameter.RAMP_ON),
                                        IntegerData(2, Parameter.RAMP_OFF)])


reportReflectedPowerParameters = Command(152, 0, 3, [IntegerData(1,Parameter.TIME_LIMIT_RF_TURN_OFF),
                                                     IntegerData(2,Parameter.POWER_LIMIT_TRIGGER)])

reportRegulationMode = Command(154, 0, 1, [MappingData({6: FORWARD_POWER,
                                                        7: LOAD_POWER,
                                                        8: EXTERNAL_POWER})])

reportActiveControlMode = Command(155, 0, 1, [MappingData({2: HOST_PORT,
                                                           4: USER_PORT,
                                                           6: FRONT_PANEL})])

reportProcessStatus = Command(162, 0, 4, [ByteFlagData([])])
