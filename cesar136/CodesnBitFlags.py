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


class Parameter(object):
    # command 151
    RAMP_ON = 'Ramp on'
    RAMP_OFF = 'Ramp off'

    # command 152
    TIME_LIMIT_RF_TURN_OFF = "time limit until RF is turned off"
    POWER_LIMIT_TRIGGER = "Power limit trigger"

    # command 154
    FORWARD_POWER = 6
    LOAD_POWER = 7
    EXTERNAL_POWER = 8

    # command 155
    HOST_PORT = 2
    USER_PORT = 4
    FRONT_PANEL = 6

    # command 162
    # byte 0
    RECIPE_RUN_ACTIVE = (0,2)
    OUTPUT_POWER = (0,5)
    RF_ON_REQUESTED = (0,6)
    SET_POINT_TOLERANCE = (0,7)

    # byte 1
    END_OF_TARGET_LIFE = (1,0)
    OVERTEMPERATURE_FAULT = (1,3)
    INTERLOCK = (1,7)

    #byte 2 and 3 reserved
    #byte 4
    DC_CURRENT_LIMIT_WARNING = (4,0)
    PROFIBUS_ERROR = (4,2)
    FAULT_PRESENT = (4,5)
    CEX_IS_LOCKED = (4,7)



