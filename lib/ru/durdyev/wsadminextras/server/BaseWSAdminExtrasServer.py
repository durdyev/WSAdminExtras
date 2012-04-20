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
# base server

from xml.dom.minidom import parse
from ru.durdyev.wsadminextras.utils.XMLUtils import XMLUtils
from ru.durdyev.wsadminextras.server.RequestHandler import RequestHandler

class BaseWSAdminExtrasServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    #profile
    _profile = None

    #subprocess
    p  = None

    #List of commands
    commandQueue = collections.deque()

    def server_activate(self):
        self.socket.listen(self.request_queue_size)
        self.startWsAdminProcess()

    def finish_request(self, request, client_address):
        self.RequestHandlerClass.__class__ = RequestHandler
        self.RequestHandlerClass(request, client_address, self, self.commandQueue)

    def startWsAdminProcess(self):

        # parsing xml config from profile
        profile_config_file = open('../profiles/' + 'SimpleProfile' + '/config/' + 'config.xml')
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
            print(out)
            if(out[:9] == 'WASX7031I'):
                print('end of loading')
            if(out[:16] == 'wait for command' or out[:9] == 'WASX7031I'):
                while True:
                    if(len(self.commandQueue) > 0):
                        command = self.commandQueue.pop()
                        #p.stdin.write('execfile(\'C:\\work\\IDEFeatures\\Python\\WSAdminWrapper\\bin\\command.jy\')\n')
                        self.p.stdin.write(command)
                        self.p.stdin.flush()
                        break
                    else:
                        print('wait 1 second')
                        time.sleep(1)

    def commandGenerator(self):
        while True:
            self.commandQueue.appendleft('execfile(\'c:\\work\\command.jy\')\n')
            time.sleep(5)

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
            self.p = subprocess.Popen(parameters['was_home'] + "\\bin\\wsadmin.sh -host " + parameters['host'] + " -port " + parameters['port'] + " -user " + parameters['username'] + " -password " + parameters['password'] + " -lang jython ", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        except IOError as e:
            logging.info(e.strerror)
            print("Cant't configuration file in profile %s " % self.profile)
            #trying to deploy list of specific files

    @property
    def profile(self):
        return self._profile