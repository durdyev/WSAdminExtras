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

import SocketServer
import subprocess
import logging
import sys
import collections
import time
import thread
import re
# base server

from xml.dom.minidom import parse
from ru.durdyev.wsadminextras.utils.XMLUtils import XMLUtils
from ru.durdyev.wsadminextras.server.RequestHandler import RequestHandler
from ru.durdyev.wsadminextras.utils.ServerSettings import ServerSettings

class BaseWSAdminExtrasServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    #profile
    _profile = None

    #subprocess
    p  = None

    #List of commands
    commandQueue = collections.deque()

    _server_settings = ServerSettings()

    def __init__(self, server_address, RequestHandler):
        RequestHandler.__class__ = RequestHandler
        SocketServer.TCPServer.__init__(self, server_address, RequestHandler, bind_and_activate=True)
        self.RequestHandlerClass.setQueue(RequestHandler, self.commandQueue)

    def server_activate(self):
        self.socket.listen(self.request_queue_size)
        self.startWsAdminProcess()

    def startWsAdminProcess(self):
        default_profile = self.server_settings.get_default_profile()

        # parsing xml config from profile
        profile_config_file = open('../profiles/' + default_profile + '/config/' + 'config.xml')
        xml_config = parse(profile_config_file)
        parameters = {}

        # was_home
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

        # call deploy script to specific OS
        if (sys.platform == 'win32'):
            self.start_win(parameters)
        else:
            self.start_nix(parameters)

        thread.start_new_thread(self.waitForCommand, ())

        #thread.start_new_thread(self.commandGenerator, ())

    def waitForCommand(self):
        while True:
            out = self.p.stdout.readline()
            errors = re.search("([A-Z]{4}[0-9]{4}[E])", out)
            print(out)
            if errors is not None:
                self.p.stdin.write("print('there are errors')\n")
                self.p.stdin.flush()
                while True:
                    out = self.p.stdout.readline()
                    print(out)
                    if "there are errors" in out:
                        break
            if(out[:9] == 'WASX7031I'):
                print('end of loading')
            if('wait for command' in out or out[:9] == 'WASX7031I' or errors is not None):
                while True:
                    if(len(self.commandQueue) > 0):
                        command = self.commandQueue.pop()
                        self.p.stdin.write(command)
                        self.p.stdin.flush()
                        break
                    else:
                        time.sleep(1)

    # deploy files to windows
    def start_win(self, parameters):
        # trying to deploy all files
        logging.info("Trying to deploy all files in %s temp directory", self.profile)

        # getting parameters from profile configuration file.
        try:
            #TODO change host-port connection to profile
            self.p = subprocess.Popen(parameters['was_home'] + "\\bin\\wsadmin.bat -host " + parameters['host'] + " -port " + parameters['port'] + " -user " + parameters['username'] + " -password " + parameters['password'] + " -lang jython ", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        except IOError as e:
            logging.info(e.strerror)
            print("Cant't configuration file in profile %s " % self.profile)
            #trying to deploy list of specific files

    #deploy files to unix
    def start_nix(self, parameters):
        # trying to deploy all files
        logging.info("Trying to deploy all files in %s temp directory", self.profile)

        # getting parameters from profile configuration file.
        try:
            #TODO change host-port connection to profile
            self.p = subprocess.Popen(parameters['was_home'] + "/bin/wsadmin.sh -host " + parameters['host'] + " -port " + parameters['port'] + " -user " + parameters['username'] + " -password " + parameters['password'] + " -lang jython ", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        except IOError as e:
            logging.info(e.strerror)
            print("Cant't configuration file in profile %s " % self.profile)
            #trying to deploy list of specific files

    @property
    def profile(self):
        return self._profile

    @property
    def server_settings(self):
        return self._server_settings