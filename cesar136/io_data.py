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

from cesar136.constants import Parameter
from cesar136.parameter import AbstractParameter


class AbstractInput(object):
    def __init__(self, parameter: AbstractParameter):
        self._param = parameter


class Output(object):
    def __init__(self, parameter: AbstractParameter, name=""):
        self._name = name
        self._parameter = parameter
        self._raw = None
        self._data = None

    def get_length(self):
        return self._parameter.get_length()

    def get_name(self):
        return self._name

    def set_raw(self, raw_data):
        self._raw = raw_data
        self._data = self.parse(raw_data)

    def parse(self, data):
        return self._parameter.parse(data)

    def get(self):
        return self._data

    def is_set(self):
        return self._data is not None

    def is_type(self, type):
        return isinstance(self._parameter, type)


class FlagOutput(Output):
    def get_bit(self, bit):
        return self._parameter.get_from(self._data, bit)


class Input(AbstractInput):
    def __init__(self, value, param: AbstractParameter):
        super(Input, self).__init__(param)
        self._data = value
        self._param.get_validator().validate(self._data)

    def get(self):
        return self._param.generate(self._data)
