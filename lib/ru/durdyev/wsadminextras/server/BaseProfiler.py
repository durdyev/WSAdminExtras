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

import logging
import os

from xml.dom.minidom import Document

# profile manager class

class BaseProfiler(object):
    #profile directory
    _profile_dir = '../profiles/'

    def __init__(self, profile_name):
        self.create_profile(profile_name)
        self.create_configuration_files(profile_name)

    def create_profile(self, profile_name):
        if profile_name is not None:
            logging.info('BaseProfiler.create_profile.'
            + 'Trying to create profile with name \'%s\'' % profile_name)
            try:
                self._profile_dir += profile_name
                os.makedirs(self._profile_dir)
                os.makedirs(self._profile_dir + '/config')
                os.makedirs(self._profile_dir + '/tmp')
            except OSError as e:
                logging.warn('Error. profile with name %s is exists' % profile_name)
                print('Can\'t create profile. Profile with same name is exists.',\
                      'Try to create profile with another name')

    def create_configuration_files(self, profile_name):
        try:
            #new configuration xml document
            doc = Document()

            #append root element
            rootElement = doc.createElement('profile')
            doc.appendChild(rootElement)

            #was home
            wasHomeElement = doc.createElement('was_home')
            rootElement.appendChild(wasHomeElement)
            wasHomeElement.appendChild(doc.createTextNode('was_home'))

            #host element
            hostElement = doc.createElement('host')
            rootElement.appendChild(hostElement)
            hostElement.appendChild(doc.createTextNode('host'))

            #port element
            portElement = doc.createElement('port')
            rootElement.appendChild(portElement)
            portElement.appendChild(doc.createTextNode('port'))

            #port element
            connTypeElement = doc.createElement('conntype')
            rootElement.appendChild(connTypeElement)
            connTypeElement.appendChild(doc.createTextNode('conntype'))

            #username element
            usernameElement = doc.createElement('username')
            rootElement.appendChild(usernameElement)
            usernameElement.appendChild(doc.createTextNode('username'))

            #password element
            passwordElement = doc.createElement('password')
            rootElement.appendChild(passwordElement)
            passwordElement.appendChild(doc.createTextNode('password'))

            #write xml to file
            file = open(self._profile_dir + '/config/' + '/config.xml', 'wb')
            file.write(doc.toprettyxml())
            file.close()
        except IOError:
            logging.info("Cant create configuration file to %s profile." % profile_name);