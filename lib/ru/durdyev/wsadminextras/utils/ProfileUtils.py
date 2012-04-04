#    WSAdminExtras is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WSAdminExtras is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

class ProfileUtils(object):

    # path to profiles directory
    _profiles_path = '../profiles/'

    def __init__(self):
        pass

    # get profile list
    def get_profile_list(self):
        profiles = []
        try:
            for profile in os.listdir(self._profiles_path):
                if os.path.isdir(self._profiles_path + profile):
                    profiles.append(profile)
        except IOError as e:
            print("Can't list in %s" % self._profiles_path)

        return profiles

