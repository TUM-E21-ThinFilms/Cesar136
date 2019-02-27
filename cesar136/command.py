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
from e21_util.interface import Loggable

from cesar136.message import MessagePacket
from cesar136.constants import *
from cesar136.io_data import *


class Command:
    def __init__(self, id, input_parameters: List[AbstractInput] = None, output_parameters: List[Output] = None):
        self._id = id
        self._input = input_parameters
        self._output = output_parameters

    def get_expected_response_data_length(self):
        return sum(map(lambda x: x.get_length(), self._output))

    def get_outputs(self):
        return self._output

    def get_raw(self):
        data = []

        for input in self._input:
            data.extend(input.get())

        bytes_to_send = len(data)

        return MessagePacket().createMessagePacket(self._id, bytes_to_send, data)
