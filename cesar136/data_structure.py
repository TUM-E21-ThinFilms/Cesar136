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

from cesar136.constants import ParamInfos, Parameter


class CSRCodes:
    UNKNOWN = -1

    ACCEPTED = 0
    CONTROL_CODE_INCORRECT = 1
    OUTPUT_ON = 2
    DATA_OUT_OF_RANGE = 4
    ACTIVE_FAULT = 7
    DATA_BYTE_COUNT_INCORRECT = 9
    RECIPE_ACTIVE = 19
    FREQUENCY_OUT_OF_RANGE = 50
    DUTY_CYCLE_OUT_OF_RANGE = 51  #
    COMMAND_NOT_DETECTED = 53
    COMMAND_NOT_ACCEPTED = 99

    CODES = [
        ACCEPTED,
        CONTROL_CODE_INCORRECT,
        OUTPUT_ON,
        DATA_OUT_OF_RANGE,
        ACTIVE_FAULT,
        DATA_BYTE_COUNT_INCORRECT,
        RECIPE_ACTIVE,
        FREQUENCY_OUT_OF_RANGE,
        DUTY_CYCLE_OUT_OF_RANGE,
        COMMAND_NOT_DETECTED,
        COMMAND_NOT_ACCEPTED,
    ]


class AbstractData(object):
    def __init__(self, name, length=1):
        self._name = name
        self._data = None
        self._length = length

    def get_length(self):
        return self._length

    def get_name(self):
        return self._name

    def clear(self):
        self._data = None

    def set_data(self, data):
        self._data = data

    def get(self):
        return self._data

    def parse(self, data):
        raise NotImplementedError()


class Response(object):
    def __init__(self, data_config: List[AbstractData]):
        self._params = data_config
        self._is_csr = False
        self._csr = CSRData()

        for config in self._params:
            if instanceof(config, CSRData):
                raise RuntimeError("CSRData is always implicitly set, do not use this in data_config.")

    def is_csr(self):
        return self._csr.is_set()

    def get_csr(self):
        return self._csr

    def set_parameter(self, data: AbstractData):
        self._params.append(data)

    def get_parameter(self, name=''):
        if self.is_csr():
            raise RuntimeError("Response contains only CSR code")

        if len(self._params) == 1:
            return self._params[0]._data

        for el in self._params:
            if isinstance(el, ByteFlagData):
                if not isinstance(name, tuple):
                    raise ValueError("Wrong parameter for Byteflag data")
                else:
                    return self._params[name[0]].get_flag(name[1])
            if el.get_name() == name:
                return el._data

        raise RuntimeError("Could not find given parameter {}".format(name))


class StringData(AbstractData):
    def __init__(self, length, name="irrelevant"):
        super(StringData, self).__init__(name, length)

    def parse(self, data):
        # get rid of empty bytes
        data = [k for k in data if k != 0]
        return bytearray(data).decode(encoding='ascii')


class IntegerData(AbstractData):
    def __init__(self, length, name="irrelevant"):
        super(IntegerData, self).__init__(name, length)

    def parse(self, data):
        return int.from_bytes(data, byteorder="little")


class MappingData(AbstractData):
    def __init__(self, mapping, name="irrelevant"):
        self._mapping = mapping
        super(MappingData, self).__init__(name, 1)

    def parse(self, data):
        # Extract DataInt from data list
        if data not in self._mapping:
            raise RuntimeError("Received unexpected value %s in mapping".format(data))

        return self._mapping[data]


class ByteFlagData(AbstractData):
    def __init__(self, name="irrelevant"):
        super(ByteFlagData, self).__init__(name, 1)

    def parse(self, data):
        return data & 0xFF

    def get_flag(self, bit_position):
        return self.get()[0] & (1 << bit_position)


class CSRData(AbstractData):
    def __init__(self):
        super(CSRData, self).__init__(Parameter.CSR, 1)

    def parse(self, data):
        if data not in CSRCodes.CODES:
            return CSRCodes.UNKNOWN

    def is_set(self):
        return self._data is not None


class AbstractInput(object):
    def __init__(self, parameter: InputParam):
        self._param = parameter


class IntegerInput(AbstractInput):
    def __init__(self, value, param: InputParam):
        super(IntegerInput, self).__init__(param)
        self._data = value
        self._param.validate(self._data)

    def get(self):
        return self._data.to_bytes(self._param.get_length(), byteorder="little")
