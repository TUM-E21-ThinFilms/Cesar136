#  Copyright (C) 2019, see AUTHORS.md
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

class ValidationError(RuntimeError):
    pass


class AbstractValidator(object):
    def validate(self, data):
        raise NotImplementedError()


class NullValidator(AbstractValidator):
    def validate(self, data):
        return True


class RangeValidator(object):
    def __init__(self, in_range):
        self._range = in_range

    def validate(self, data):
        if data not in self._range:
            raise ValidationError("Data {} not in range {}".format(data, self._range))
