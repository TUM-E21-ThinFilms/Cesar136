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


class AbstractData(object):
    def __init__(self, name=''):
        self._name = name
        self._data = None

    def get_name(self):
        return self._name

    def set_data(self, data):
        self._data = data

    def get(self):
        return self._data


class ResponseFormat(object):
    def __init__(self):
        self._params = []

    def set_parameter(self, data: AbstractData):
        self._params.append(data)

    def get_parameter(self, name=''):
        if len(self._params) == 1:
            return self._params[0]._data

        for el in self._params:
            if isinstance(el, ByteFlagData):
                if isinstance(name, tuple):
                    raise ValueError("Wrong parameter for Byteflag data")
                else:
                    return self._params[name[0]].get_flag(name[1])
            if el.get_name() == name:
                return el._data

        raise RuntimeError("Could not find given parameter {}".format(name))


# any additional new datatype has to contain the instance _numberOfBytes
# and the function analyze()

class StringData(AbstractData):
    def __init__(self, NumberOfBytes, name="irrelevant"):
        super(StringData, self).__init__(name)
        self._numberOfBytes = NumberOfBytes

    def analyze(self, Intlist):
        # get rid of empty bytes
        Intlist = [k for k in Intlist if k != 0]
        self.set_data(bytearray(Intlist).decode(encoding='ascii'))


class IntegerData(AbstractData):
    def __init__(self, NumberOfBytes, name="irrelevant"):
        self._numberOfBytes = NumberOfBytes
        super(IntegerData, self).__init__(name)

    def analyze(self, Intlist):
        self.set_data(int.from_bytes(Intlist, byteorder="little"))


class MappingData(AbstractData):
    def __init__(self, mapping, name="irrelevant"):
        self._mapping = mapping
        self._numberOfBytes = 1
        super(MappingData, self).__init__(name)

    def analyze(self, data):
        # Extract DataInt from data list
        DataInt = data[0]
        if not DataInt in self._mapping:
            # try to find the value in the CSR responses if it is not in the mapping
            if not DataInt in CSRCodes:
                raise ValueError("Ceasar unit returned different value than expected")
            self.set_data(CSRCodes[DataInt])
        else:
            self.set_data(self._mapping[DataInt])


class ByteFlagData(AbstractData):
    def __init__(self, name="irrelevant"):
        # self._bitFlagList = BitFlagList
        self._numberOfBytes = 1
        super(ByteFlagData, self).__init__(name)

    def analyze(self, data):
        self.set_data(data)

    def get_flag(self, bit_position):
        return self.get()[0] & (1 << bit_position)
