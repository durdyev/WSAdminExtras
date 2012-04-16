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

from PyQt4 import QtGui
from PyQt4 import QtCore
from ru.durdyev.wsadminextras.utils.ServerSettings import ServerSettings

class ServerSettingsWidget(QtGui.QWidget):

    # server settings xml
    _server_settings = ServerSettings()

    def __init__(self, parent = None):
        super(ServerSettingsWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.serverSettingsGridLayout = QtGui.QGridLayout()
        serverSettingsWidget = QtGui.QWidget(self)
        serverSettingsWidget.setGeometry(0, 0, 340, 90)
        serverSettingsWidget.setLayout(self.serverSettingsGridLayout)

        # server address
        self.serverSettingsGridLayout.addWidget(QtGui.QLabel("Server address"), 0, 0)
        serverAddress = QtCore.QString(self._server_settings.get_server_address())
        self.serverAddressInput = QtGui.QLineEdit(serverAddress)
        self.serverSettingsGridLayout.addWidget(self.serverAddressInput, 0, 1)

        # server port
        self.serverSettingsGridLayout.addWidget(QtGui.QLabel("Server port"), 1, 0)
        serverPort = QtCore.QString(self._server_settings.get_server_port())
        self.serverPortInput = QtGui.QLineEdit(serverPort)
        self.serverSettingsGridLayout.addWidget(self.serverPortInput, 1, 1)

        # buttons
        updateButton = QtGui.QPushButton("Update server settings")
        updateButton.clicked.connect(self.updateServerSettings)
        self.serverSettingsGridLayout.addWidget(updateButton, 2 , 0)

    def updateServerSettings(self):
        params = {
            "address" : str(self.serverAddressInput.text()),
            "port" : str(self.serverPortInput.text())
        }

        if self._server_settings.update_server_settings(params) == 0:
            QtGui.QMessageBox.information(self, QtCore.QString("Message"),
                QtCore.QString("Server configuration successfully updated."))