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

import os, logging

from xml.dom import minidom
from xml.dom.minidom import Document

class ServerSettings(object):

    _server_config_file = "../config/server.xml"

    def __init__(self):
        pass

    def get_server_address(self):
        serverSettings = minidom.parse(self._server_config_file)
        return serverSettings.getElementsByTagName("address")[0].firstChild.data.strip()

    def get_server_port(self):
        serverSettings = minidom.parse(self._server_config_file)
        return serverSettings.getElementsByTagName("port")[0].firstChild.data.strip()

    def get_default_profile(self):
        serverSettings = minidom.parse(self._server_config_file)
        return serverSettings.getElementsByTagName("default_profile")[0].firstChild.data.strip()

    def update_server_settings(self, params):
        if params is not None:
            try:
                doc = Document()

                rootElement = doc.createElement("server")

                # address
                addressElement = doc.createElement("address")
                addressElement.appendChild(doc.createTextNode(params['address']))
                rootElement.appendChild(addressElement)

                #port
                portElement = doc.createElement("port")
                portElement.appendChild(doc.createTextNode(params['port']))
                rootElement.appendChild(portElement)

                #port
                defaultProfileElement = doc.createElement("default_profile")
                defaultProfileElement.appendChild(doc.createTextNode(params['default_profile']))
                rootElement.appendChild(defaultProfileElement)

                doc.appendChild(rootElement)

                file = open(self._server_config_file, 'wb')
                file.write(doc.toprettyxml())
                file.close()

                return 0
            except IOError as e:
                logging.warning("Can't update configuration file.")

            return - 1