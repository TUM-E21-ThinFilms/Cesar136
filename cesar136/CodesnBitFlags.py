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

# command 154
FORWARD_POWER = 6
LOAD_POWER = 7
EXTERNAL_POWER = 8

# command 155
HOST_PORT =2
USER_PORT = 4
FRONT_PANEL = 6

#command 162
RECIPE_RUN_IS_ACTIVE = 2
OUTPUT_POWER = 5
[RESERVERD, UNASSIGNED, RECIPE_RUN_IS_ACTIVE, RESERVED, RESERVED,
 OUTPUT_POWER, RF_ON_REQUESTED, SET_POINT_TOLERANCE]=list(range(0, 8))

class Parameter(object):
    # command 151
    RAMP_ON = 'Ramp on'
    RAMP_OFF = 'Ramp off'

    # command 152
    TIME_LIMIT_RF_TURN_OFF = "time limit until RF is turned off"
    POWER_LIMIT_TRIGGER = "Power limit trigger"
