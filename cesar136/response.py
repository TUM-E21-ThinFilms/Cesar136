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

from cesar136.constants import Parameter
from cesar136.io_data import Output

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

    def get_parameter(self, type_or_name=None):
        if self.is_csr():
            raise RuntimeError("Response contains only CSR code")

        if len(self._params) == 1 and type_or_name is None:
            return self._params[0]

        if isinstance(type_or_name, (int, str)):
            for el in self._params:
                if el.get_name() == type_or_name:
                    return el
        elif type_or_name is not None:
            for el in self._params:
                if el.is_type(type_or_name):
                    return el
        else:
            raise RuntimeError("No selector given")

        raise RuntimeError("Could not find given parameter {}".format(type_or_name))
