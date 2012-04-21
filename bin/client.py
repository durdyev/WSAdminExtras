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
import os
import socket
import baseFunc

from ru.durdyev.wsadminextras.utils.NetUtils import NetUtils
from ru.durdyev.wsadminextras.utils.ServerHeaders import ServerHeaders

HOST, PORT = '127.0.0.1', 1061
RESPONSE_LEN = 2
delim_n = '\n'
server_headers = ServerHeaders()

#entry point
def main():
    key = sys.argv[1]
    # if command is upload
    if key == '-upload':
        file_url = sys.argv[2]

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((HOST, PORT))
        basename = os.path.basename(file_url)
        filename, filetype = os.path.splitext(basename)

        f = open(file_url, 'rb')

        request_data = 'Command:UPLOAD' + delim_n
        request_data += 'Content-length:' + str(os.path.getsize(file_url)) + delim_n
        request_data += 'Content-type:' + filetype + delim_n
        request_data += 'Filename:' + basename + delim_n
        request_data += 'Profile:SimpleProfile' + delim_n
        request_data += ' ' * (server_headers.headers_len - len(request_data))
        connection.sendall(request_data)
        connection.sendall(f.read())
        connection.close()
        f.close()

    # if command is deploy
    if key == '-deploy':
        profile_name = sys.argv[2]
        deploy_file_list = sys.argv[3]

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((HOST, PORT))

        request_content = str(deploy_file_list)

        request_data = "Command:DEPLOY" + delim_n
        request_data += "Profile:" + profile_name + delim_n
        request_data += "Content-length:" + str(len(request_content)) + delim_n
        request_data += "Content-type: plain-text"
        request_data += "Mode: Reinstall"
        request_data += ' ' * (server_headers.headers_len - len(request_data))
        connection.sendall(request_data)
        connection.sendall(request_content)

    # command get file list from tmp profile
    if key == '-filelist':
        profile_name = sys.argv[2]

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((HOST, PORT))

        request_data = "Command:FILELIST" + delim_n
        request_data += "Profile:" + profile_name + delim_n
        request_data += "Content-length:" + str(0)
        request_data += "Content-type: plain-text"
        request_data += ' ' * (server_headers.headers_len - len(request_data))
        connection.sendall(request_data)

        files_str = ''
        while True:
            data = connection.recv(1024)
            if not data: break
            files_str += data

        files = files_str.split(';')

    #clear logs
    if key == '-clearlogs':
        profile_name = sys.argv[2]

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((HOST, PORT))

        request_data = "Command:CLEARLOGS" + delim_n
        request_data += "Profile:" + profile_name + delim_n
        request_data += "Content-length:" + str(0)
        request_data += "Content-type: plain-text"
        request_data += ' ' * (server_headers.headers_len - len(request_data))
        connection.sendall(request_data)

    if key == '-custom':
        # example
        #-custom SimpleProfile uninstall "{ [node_name:node1], [server_name:server1], [application_name:loan-01] }"

        profile_name = sys.argv[2]
        template = sys.argv[3]
        parameters = sys.argv[4]

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((HOST, PORT))

        request_data = "Command:CUSTOM" + delim_n
        request_data += "Profile:" + profile_name + delim_n
        request_data += "Content-length:" + str(len(parameters)) + delim_n
        request_data += "Content-type:plain-text" + delim_n
        request_data += "Template:" + template + delim_n
        request_data += "Parameters:" + parameters + delim_n
        request_data += ' ' * (server_headers.headers_len - len(request_data))

        connection.sendall(request_data)
        connection.close()

if __name__ == '__main__':
    main()
