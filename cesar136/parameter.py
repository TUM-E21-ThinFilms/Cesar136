# Copyright (C) 2016, see AUTHORS.md
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


from cesar136.validator import AbstractValidator, RangeValidator


class AbstractParameter(object):
    def __init__(self, length, validator):
        self._length = length
        self._validator = validator

    def get_length(self):
        return self._length

    def get_validator(self) -> AbstractValidator:
        return self._validator

    def generate(self, data):
        data = int(data)
        return int(data).to_bytes(self._length, byteorder="little")

    def parse(self, raw_data):
        return int.from_bytes(raw_data, byteorder="little")


class ByteFlagParameter(AbstractParameter):
    def get_from(self, data, bit):
        return data & (1 << 8 * bit[0] + bit[1])


class StringParameter(AbstractParameter):
    def generate(self, data):
        return str(data).encode("ascii")

    def parse(self, raw_data):
        data = [k for k in raw_data if k != 0]
        return bytearray(data).decode(encoding='ascii')


class RangeParameter(AbstractParameter):
    def __init__(self, length):
        super(RangeParameter, self).__init__(length, RangeValidator(self.RANGE))
