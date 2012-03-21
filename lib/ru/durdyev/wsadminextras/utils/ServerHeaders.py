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

#server headers
class ServerHeaders(object):
    #headers len is 300 bytes
    _headers_len = 300

    @property
    def headers_len(self):
        return self._headers_len

    @property
    def request_id(self):
        return 'RequestID:'

    @property
    def command(self):
        return 'Command:'

    @property
    def content_len(self):
        return 'Content-length:'

    @property
    def content_type(self):
        return 'Content-type:'

    @property
    def filename(self):
        return 'Filename:'

    @property
    def profile(self):
        return 'Profile:'

    @property
    def response_code(self):
        return 'Response-code:'
    
    