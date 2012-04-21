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
from ru.durdyev.wsadminextras.utils.TemplateParser import TemplateParser
from ru.durdyev.wsadminextras.utils.AdditionalParameters import AdditionalParameters
from ru.durdyev.wsadminextras.exceptions.HeadersNotSetException import HeadersNotSetException
from ru.durdyev.wsadminextras.exceptions.ProfileNotFoundException import ProfileNotFoundException

#base event handler class
#when server recive a command, this handler call a command handler method
class RequestEventHandler(RequestHandler):
    #server codes
    _server_codes = ServerCodes()

    # additional parameters
    _additional_params = AdditionalParameters()

    #trying to upload a file
    def UPLOAD_handler(self):
        logging.info("uploading a file. request_id=%s" % self.request_id)
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

    def FILELIST_handler(self):
        logging.info(('Trying to get file list from %s temp directory.' % self.profile))
        print('Trying to get file list from %s temp directory.' % self.profile)

        profile_tmp_dir = '../profiles/%s/tmp' % self.profile
        files = os.listdir(profile_tmp_dir)
        serializable_files = ''
        if len(files) > 0:
            for file in files:
                serializable_files += "%s;" % file

            if len(serializable_files) > 0 :
                self.request.sendall(serializable_files)

    def CLEARLOGS_handler(self):
        logging.info('Trying to clear logs in profile %s' % self.profile)
        print('Trying to clear logs in profile %s' % self.profile)

        # parsing xml config from profile
        profile_config_file = open('../profiles/' + self.profile + '/config/' + 'config.xml')
        xml_config = parse(profile_config_file)

        # logs directories
        logsFoldersElement = xml_config.getElementsByTagName('logs_folders')
        logsFolders = logsFoldersElement[0].firstChild.nodeValue.strip().split(',')
        for logFolder in logsFolders:
            try:
                if len(logFolder) > 0:
                    for file in os.listdir(logFolder.strip()):
                        os.remove(file)
            except OSError as e:
                errormessage = 'Cant delete files in %s.' % logFolder.strip()
                print(errormessage)
                logging.info(errormessage)

    def CUSTOM_handler(self):
        templateParser = TemplateParser()

        regexp_template = re.search('.*Template:(.*).*', self.headers)
        regexp_parameters = re.search('.*Parameters:(.*).*', self.headers)

        template = None
        parameters = None
        if regexp_template is not None:
            template = regexp_template.group(1).strip()
        if regexp_parameters is not None:
            parameters = regexp_parameters.group(1).strip()


        command = templateParser.generateScriptFromTemplate(template, self.parseParameters(parameters), self.profile)
        self.wsadminQueue.appendleft(command)

    # parse custom parameters
    def parseParameters(self, parameterStr):
        parameters_dict = {}
        if parameterStr is not None:
            regexp_params = re.findall("\[([aA-zZ0-9]+\:[aA-zZ0-9.-]+)\]", parameterStr)
            if regexp_params is not None:
                for p in regexp_params:
                    param_regexp = re.search("([aA-zZ0-9]+)\:([aA-zZ0-9.-]+)", p)
                    if param_regexp is not None:
                        parameters_dict[param_regexp.group(1)] = param_regexp.group(2)

        return parameters_dict

    @property
    def server_codes(self):
        return self._server_codes