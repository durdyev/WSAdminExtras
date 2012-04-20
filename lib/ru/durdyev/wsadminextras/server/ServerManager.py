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

from ru.durdyev.wsadminextras.server.BaseWSAdminExtrasServer import BaseWSAdminExtrasServer

class ServerManager(object):

    _instance = None

    _server = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ServerManager, cls).__new__(
                cls, *args, **kwargs)

        return cls._instance

    def startServer(self):
        self._server = BaseWSAdminExtrasServer()
        pass

    def stopServer(self):
        pass

    def serverStatus(self):
        pass