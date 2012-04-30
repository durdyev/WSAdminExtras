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

class ServerMessages(object):

    # file uploaded
    _file_uploaded_msg = "File %s succesfully uploaded."

    # custom command completed
    _custom_command_completed_msg = "Custom command completed"

    def __init__(self):
        pass

    @property
    def file_uploaded_msg(self):
        return self._file_uploaded_msg

    @property
    def custom_command_completed_msg(self):
        return self._custom_command_completed_msg

