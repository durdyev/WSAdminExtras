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

#this class contains server codes
class ServerCodes(object):
    #ok
    _code_ok = '200'

    #code_headers recived
    _code_headers_recived = '100'

    #code_headers_not_recived
    _code_headers_not_recived = '700'

    #profile not found code
    _code_profile_not_found = '610'

    def __init__(self):
        pass

    @property
    def code_ok(self):
        return self._code_ok

    @property
    def code_headers_recived(self):
        return self._code_headers_recived

    @property
    def code_headers_not_recived(self):
        return self._code_headers_not_recived

    @property
    def code_profile_not_found(self):
        return self._code_profile_not_found