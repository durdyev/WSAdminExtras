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
import os
import logging
import sys
from xml.dom.minidom import parse
from ru.durdyev.wsadminextras.server.RequestHandler import RequestHandler
from ru.durdyev.wsadminextras.utils.ServerCodes import ServerCodes
from ru.durdyev.wsadminextras.utils.NetUtils import NetUtils
from ru.durdyev.wsadminextras.utils.ServerHeaders import ServerHeaders
from ru.durdyev.wsadminextras.utils.XMLUtils import XMLUtils
from ru.durdyev.wsadminextras.utils.AdditionalParameters import AdditionalParameters
from ru.durdyev.wsadminextras.exceptions.HeadersNotSetException import HeadersNotSetException
from ru.durdyev.wsadminextras.exceptions.ProfileNotFoundException import ProfileNotFoundException

#base event handler class
#when server recive a command, this handler call a command handler method
class RequestEventHandler(RequestHandler):
    #server codes
    _server_codes = ServerCodes()

    # xml utils
    _xml_utils = XMLUtils()

    # additional parameters
    _additional_params = AdditionalParameters()

    # path to jython script file linux
    _jython_nix = "sh ../scripts/jython.sh"

    # path to jython script win
    _jython_win = "..\scripts\jython.bat"

    #trying to upload a file
    def UPLOAD_handler(self):
        logging.info("uploading a file. request_id=")
        self._request_id = NetUtils.generate_request_id()
        code = self.server_codes.code_ok
        filename = ''

        filename_regexp = re.search(".*Filename:(.*).*", self.headers)
        if filename_regexp is not None:
            filename = filename_regexp.group(1).strip()
        else:
            raise HeadersNotSetException(server_codes.code_headers_not_recived,
                                         'filename not set.')
        response_headers = {
            self.server_headers.request_id: self.request_id + NetUtils.delimeter_n(),
            self.server_headers.response_code: code + NetUtils.delimeter_n()
        }

        # if profile not exist raise exception
        if not os.path.exists('../profiles/' + self.profile):
            raise ProfileNotFoundException(self.server_codes.code_profile_not_found,
                                           'Profile ' + self.profile + 'doesn\'t exists')

        f = open('../profiles/' + self.profile + '/tmp/' + filename, 'wb')
        while True:
            file_data = self.request.recv(1024)
            if not file_data: break
            f.write(file_data)
        f.close()

        self.send_response(response_headers, None)

    # deploy uploaded file to server
    def DEPLOY_handler(self):
        deploy_files = self.request.recv(self.content_len)
        deploy_file_list = deploy_files.split(',')
        mode_regexp = filename_regexp = re.search(".*Mode:(.*).*", self.headers)

        # parsing xml config from profile
        profile_config_file = open('../profiles/' + self.profile + '/config/' + 'config.xml')
        xml_config = parse(profile_config_file)
        parameters = {}

        # mode
        if mode_regexp is not None:
            parameters['mode'] = mode_regexp.group(1).strip()

        # host address
        hostElements = xml_config.getElementsByTagName('was_home')
        parameters['was_home'] = hostElements[0].firstChild.nodeValue.strip()

        # host address
        hostElements = xml_config.getElementsByTagName('host')
        parameters['host'] = hostElements[0].firstChild.nodeValue.strip()

        # port number
        portElements = xml_config.getElementsByTagName('port')
        parameters['port'] =  portElements[0].firstChild.nodeValue.strip()

        # username
        userNameElements = xml_config.getElementsByTagName('username')
        parameters['username'] = userNameElements[0].firstChild.nodeValue.strip()

        # password element
        passwordElements = xml_config.getElementsByTagName('password')
        parameters['password'] = passwordElements[0].firstChild.nodeValue.strip()

        # files
        parameters['files'] = deploy_file_list

        # call deploy script to specific OS
        if (sys.platform == 'win32'):
            self.deploy_win(parameters)
        else:
            self.deploy_nix(parameters)


    # deploy files to windows
    def deploy_win(self, parameters):
        deploy_file_list = parameters['files']

        # trying to deploy all files
        if len(deploy_file_list) <= 1 and deploy_file_list[0] == 'ALL':
            logging.info("Trying to deploy all files in %s temp directory", self.profile)
            print('Deploy all files from temp directory to WS')

            # getting parameters from profile configuration file.
            try:
                if parameters['mode'] == self._additional_params.mode_reinstall:
                    profile_temp_path = '../profiles/' + self.profile + '/tmp/'
                    files = os.listdir(profile_temp_path)
                    for file in files:
                        abs_file_path = os.path.abspath(profile_temp_path + file)
                        file_name = os.path.splitext(file)[0]
                        command = self._jython_win + " "
                        command += parameters['was_home'] + " "
                        command += parameters['host'] + " "
                        command += parameters['port'] + " "
                        command += parameters['username'] + " "
                        command += parameters['password'] + " "
                        command += parameters['mode'] + " "
                        command += abs_file_path + " "
                        command += file_name + " "
                        command += '"[ [] ]"'
                        print(command)
                        os.system(command)
            except IOError as e:
                logging.info(e.strerror)
                print("Cant't configuration file in profile %s " % self.profile)
                #trying to deploy list of specific files
        else:
            for file in deploy_file_list:
                logging.info("Trying to deploy %s", file)
                print('deploy ' + file.strip() + ' to ws')

    #deploy files to unix
    def deploy_nix(self, parameters):
        deploy_file_list = parameters['files']

        # trying to deploy all files
        if len(deploy_file_list) <= 1 and deploy_file_list[0] == 'ALL':
            logging.info("Trying to deploy all files in %s temp directory", self.profile)
            print('Deploy all files from temp directory to WS')

            # getting parameters from profile configuration file.
            try:
                pass
            except IOError as e:
                logging.info(e.strerror)
                print("Cant't configuration file in profile %s " % self.profile)
                #trying to deploy list of specific files
        else:
            for file in deploy_file_list:
                logging.info("Trying to deploy %s", file)
                print('deploy ' + file.strip() + ' to ws')

    @property
    def server_codes(self):
        return self._server_codes