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

import re
import logging
import SocketServer
from ru.durdyev.wsadminextras.exceptions.HeadersNotSetException import HeadersNotSetException
from ru.durdyev.wsadminextras.utils.ServerCodes import ServerCodes
from ru.durdyev.wsadminextras.utils.ServerCommands  import ServerCommands
from ru.durdyev.wsadminextras.exceptions.BaseException import BaseException
from ru.durdyev.wsadminextras.utils.NetUtils import NetUtils
from ru.durdyev.wsadminextras.utils.ServerHeaders import ServerHeaders

# base request handler class.
class RequestHandler(SocketServer.StreamRequestHandler):
    #request_id
    _request_id = None

    #comand
    _command = None

    #headers
    _headers = None

    #content len
    _content_len = None

    #content type
    _content_type = None

    #profile
    _profile = None

    _server_commands = ServerCommands()
    _server_codes = ServerCodes()
    _server_headers = ServerHeaders()

    _wsadminQueue = None

    def __init__(self, request, client_address, server, queue):
        self._wsadminQueue = queue
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)

    #override method to catch a packets.
    def handle(self):
        self._request_id = NetUtils.generate_request_id()
        self._headers = self.request.recv(self._server_headers.headers_len)

        regexp_headers = re.search('.*Command:(.*).*', self.headers)
        regexp_content_len = re.search(".*Content-length:(.*).*", self.headers)
        regexp_content_type = re.search(".*Content-type:(.*).*", self.headers)
        regexp_profile = re.search(".*Profile:(.*).*", self.headers)
        try:
            if regexp_content_len is not None:
                self._content_len = regexp_content_len.group(1).strip()
            else:
                raise HeadersNotSetException(self.server_codes.code_headers_not_recived,
                                             'Content-len not is not recived.')

            if regexp_content_type is not None:
                self._content_type = regexp_content_type.group(1).strip()
            else:
                raise HeadersNotSetException(self.server_codes.code_headers_not_recived,
                                             'Content-type is not recived')

            if regexp_profile is not None:
                self._profile = regexp_profile.group(1).strip()
            else:
                raise HeadersNotSetException(self.server_codes.code_headers_not_recived,
                                             'Profile not recived.')

            if regexp_headers is not None:
                comand_code = regexp_headers.group(1).strip()
                if len(comand_code) > 0:
                    self._command = comand_code + '_handler'
                else:
                    logging.info('command doesn\'t set. ')
                    raise HeadersNotSetException(server_codes.code_headers_not_recived,
                                                 'command is not set.')

                commandHandler = getattr(self, self.command)
                if commandHandler is not None:
                    commandHandler()
                else:
                    self.send_error(server_codes.code_headers_not_recived)

            return
        except BaseException as e:
            #headers not recived
            logging.info('Headers not set error.' + e.msg)
            self.send_error(self.server_codes.code_headers_not_recived)
            return


    #recv bytes
    @classmethod
    def recv_bytes(cls, begin, end):
        size = 1
        output = ''
        while size <= end:
            if size >= begin <= end:
                output += self.request.recv(size - len(output))
            size += 1

        return output

    #send response to the client
    def send_response(self, headers, data):
        response_headers = ''
        for key in headers:
            response_headers += key + headers[key]

        self.request.send(response_headers)
        if data is not None:
            self.request.send(data)

    #sending an error
    def send_error(self, error_code):
        response_data = self.request_id
        response_data += self.request_id + NetUtils.delimeter_n()
        response_data += self.server_headers.response_code + error_code
        response_data += str(NetUtils.delimeter_n())
        self.request.send(response_data)

    @property
    def request_id(self):
        return self._request_id

    @property
    def command(self):
        return self._command

    @property
    def headers(self):
        return self._headers

    @property
    def content_len(self):
        return int(self._content_len)

    @property
    def content_type(self):
        return self._content_type

    @property
    def profile(self):
        return self._profile

    @property
    def headers(self):
        return self._headers

    @property
    def server_headers(self):
        return self._server_headers

    @property
    def server_codes(self):
        return self._server_codes

    @property
    def server_commands(self):
        return self._server_commands

    @property
    def wsadminQueue(self):
        return self._wsadminQueue