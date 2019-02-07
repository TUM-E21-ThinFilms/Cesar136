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


class AbstractData(object):
    def __init__(self, name=''):
        self._name = name
        self._data = None

    def get_name(self):
        return self._name

    def set_data(self, data):
        self._data = data


class ResponseFormat(object):
    def __init__(self):
        self._params = []

    def set_parameter(self, data: AbstractData):
        self._params.append(data)

    def get_parameter(self, name=''):

        if len(self._params) == 1:
            return self._params[0]

        for el in self._params:
            if el.get_name() == name:
                return el

        raise RuntimeError("Could not find given parameter {}".format(name))


# any additional new datatype has to contain the instance _numberOfBytes
# and the function analyze()

class StringData(AbstractData):
    def __init__(self, NumberOfBytes, name="irrelevant"):
        super(StringData, self).__init__(name)
        self._numberOfBytes = NumberOfBytes

    def get(self):
        return self.analyze(self._data)

    def analyze(self, Intlist):
        # get rid of empty bytes
        Intlist = [k for k in Intlist if k != 0]
        return bytearray(Intlist).decode(encoding='ascii')


class IntegerData(AbstractData):
    def __init__(self, NumberOfBytes, name="irrelevant"):
        self._numberOfBytes = NumberOfBytes
        super(IntegerData, self).__init__(name)

    def analyze(self, Intlist):
        return int.from_bytes(Intlist, byteorder="little")


class MappingData(AbstractData):
    def __init__(self, mapping, name="irrelevant"):
        self._mapping = mapping
        self._numberOfBytes = 1
        super(MappingData, self).__init__(name)

    def analyze(self, data):
        # Extract DataInt from data list
        DataInt = data[0]
        if not DataInt in self._mapping:
            raise ValueError("Ceasar unit returned different value than expected")
        return self._mapping[DataInt]


class ByteFlagData(AbstractData):
    def __init__(self, BitFlagList, name="irrelevant"):  # [RESERVED, RESERVED, RECIPE_IS_ACTIVE, ...]
        self._bitFlagList = BitFlagList
        self._numberOfBytes = 1
        super(ByteFlagData, self).__init__(name)

    def analyze(self, data):
        return data

    def get_flag(self, bit_position):
        return self.get() & (1 << bit_position)
