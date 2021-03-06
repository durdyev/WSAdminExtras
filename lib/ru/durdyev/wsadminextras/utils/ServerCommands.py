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

class ServerCommands(object):
    # when client trying to upload a file.
    _command_UPLOAD = "UPLOAD"

    _command_DEPLOY = "DEPLOY"

    _command_CUSTOM = "CUSTOM"

    _command_CLEARLOGS = "CLEARLOGS"

    def __init__(self):
        pass

    @property
    def command_UPLOAD(self):
        return self._command_UPLOAD

    @property
    def command_DEPLOY(self):
        return self._command_DEPLOY

    @property
    def command_CUSTOM(self):
        return self._command_CUSTOM

    @property
    def command_CLEARLOGS(self):
        return self.command_CLEARLOGS
