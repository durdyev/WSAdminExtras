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

import sys

sys.path.append("../lib")
import  logging, threading
import baseFunc

from ru.durdyev.wsadminextras.server.BaseWSAdminExtrasServer import BaseWSAdminExtrasServer
from ru.durdyev.wsadminextras.server.RequestEventHandler import RequestEventHandler
from ru.durdyev.wsadminextras.utils.ServerCodes import ServerCodes

#starting the server
#entry point
def main():
    try:
        baseFunc.configure_logging()

        logging.info('Starting a server')
        HOST, PORT = '', 1060
        server = BaseWSAdminExtrasServer((HOST, PORT), RequestEventHandler)
        server.allow_reuse_address = True

        print('Server now running at ' + str(server.server_address))
        logging.info(('Server now running at ' + str(server.server_address)))

        server.serve_forever()

    except IOError as e:
        print('logging folder doesn\'t exist')
        print('trying to create logging folder...')
        if baseFunc.create_log_folder():
            baseFunc.configure_logging()
    except KeyboardInterrupt as e:
        print("Server stoped.")

if __name__ == '__main__':
    main()
