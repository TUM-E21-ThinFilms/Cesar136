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

from cesar136.constants import ParamInfos, Parameter, AbstractParameter


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

    def is_type(self, type):
        return instanceof(self._parameter, type)


class FlagOutput(Output):
    def get(self, bit):
        return self._parameter.get_from(self._data, bit)


class Response(object):
    def __init__(self, outputs: List[Output]):
        self._params = outputs
        self._is_csr = False
        self._csr = Output(Parameter.CSRCode())

        for config in self._params:
            if config.is_type(Parameter.CSRCode):
                raise RuntimeError("CSRCode is always implicitly set, do not use this in data_config.")

    def is_csr(self):
        return self._csr.is_set()

    def get_csr(self):
        return self._csr

    def set_parameter(self, data: Output):
        self._params.append(data)

    def get_parameter(self, type_or_name=''):
        if self.is_csr():
            raise RuntimeError("Response contains only CSR code")

        if len(self._params) == 1:
            return self._params[0]._data

        if isinstance(type_or_name, string):
            for el in self._params:
                if el.get_name() == type_or_name:
                    return el
        else:
            for el in self._params:
                if el.is_type(type_or_name):
                    return el

        raise RuntimeError("Could not find given parameter {}".format(name))


class AbstractInput(object):
    def __init__(self, parameter: AbstractParameter):
        self._param = parameter


class Input(AbstractInput):
    def __init__(self, value, param: AbstractParameter):
        super(Input, self).__init__(param)
        self._data = value
        self._param.get_validator().validate(self._data)

    def get(self):
        return self._param.generate(self._data)
