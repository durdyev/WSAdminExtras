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
from ru.durdyev.wsadminextras.ui.utils.WidgetModes import WidgetModes
from ru.durdyev.wsadminextras.server.BaseProfiler import BaseProfiler

class CreateProfileWidget(QtGui.QWidget):

    # base grid layout
    _gridLayout = QtGui.QGridLayout()

    # widget mode
    _mode = None

    _widget_modes = WidgetModes()

    def __init__(self, parent=None, mode=None):
        super(CreateProfileWidget,self).__init__(parent)
        self.mode = mode
        self.initUI()
        self.initBaseUI()

    # initialize widget
    def initUI(self):
        self.setWindowTitle('Create new profile')
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setGeometry(400, 220, 300, 200)
        self.setLayout(self._gridLayout)
        self.show()

    # initialize base ui (form, buttons etc)
    def initBaseUI(self):
        # profile name
        self._gridLayout.addWidget(QtGui.QLabel('Profile name:'), 0, 1)
        self.profileNameInput = QtGui.QLineEdit()
        self._gridLayout.addWidget(self.profileNameInput, 0, 2)

        # profile parameters
        self._gridLayout.addWidget(QtGui.QLabel('WAS Home:'), 1, 1)
        self.wasHomeInput = QtGui.QLineEdit()
        self._gridLayout.addWidget(self.wasHomeInput, 1, 2)

        # profile host
        self._gridLayout.addWidget(QtGui.QLabel('Host:'), 2, 1)
        self.hostInput= QtGui.QLineEdit()
        self._gridLayout.addWidget(self.hostInput, 2, 2)

        # profile port
        self._gridLayout.addWidget(QtGui.QLabel('Port:'), 3, 1)
        self.portInput = QtGui.QLineEdit()
        self._gridLayout.addWidget(self.portInput, 3, 2)

        # profile connection type
        self._gridLayout.addWidget(QtGui.QLabel('Connection type:'), 4, 1)
        self.connectionTypeInput = QtGui.QLineEdit()
        self._gridLayout.addWidget(self.connectionTypeInput, 4, 2)

        # profile admin users
        self._gridLayout.addWidget(QtGui.QLabel('Admin user:'), 5, 1)
        self.adminUserInput = QtGui.QLineEdit()
        self._gridLayout.addWidget(self.adminUserInput, 5, 2)

        # profile admin user
        self._gridLayout.addWidget(QtGui.QLabel('Password:'), 6, 1)
        self.passwordInput = QtGui.QLineEdit()
        self._gridLayout.addWidget(self.passwordInput, 6, 2)

        if (self.mode == WidgetModes.create_mode):
            #create button
            self.createButton = QtGui.QPushButton('Create')
            self._gridLayout.addWidget(self.createButton, 7, 1)
            self.createButton.clicked.connect(self.createNewProfileAction)

        if (self.mode == WidgetModes.update_mode):
            #update button
            self.updateButton = QtGui.QPushButton('Update')
            self._gridLayout.addWidget(self.updateButton, 7, 1)
            self.updateButton.clicked.connect(self.updateProfileAction)

        #close button
        self.closeButton = QtGui.QPushButton('Close')
        self._gridLayout.addWidget(self.closeButton, 7, 2)
        self.closeButton.clicked.connect(self.closeAction)

    def closeAction(self):
        for i in reversed(range(self._gridLayout.count())):
            item = self._gridLayout.itemAt(i)
            self._gridLayout.removeItem(item)

        self.close()

    def createNewProfileAction(self):
        profileParameters = {} # map with parameters
        profileName = str(self.profileNameInput.text())
        profileParameters['profile_name'] = profileName
        profileParameters['was_home'] = str(self.wasHomeInput.text())
        profileParameters['host'] = str(self.hostInput.text())
        profileParameters['port'] = str(self.portInput.text())
        profileParameters['conntype'] = str(self.connectionTypeInput.text())
        profileParameters['username'] = str(self.adminUserInput.text())
        profileParameters['password'] = str(self.passwordInput.text())

        ## creating profile
        if not self.validateParameters(profileParameters):
            baseProfiler = BaseProfiler()
            baseProfiler.create_profile(profileName)
            baseProfiler.create_configuration_file(profileName, profileParameters)
            self.emit(QtCore.SIGNAL("profileCreated(QString)"), profileName)

    def validateParameters(self, profileParameters):
        error = False
        errorMessages = ""
        if len(profileParameters['profile_name']) <= 0:
            errorMessages += "<li>Profile name is not set</li>"
            error = True
        if len(profileParameters['was_home']) <= 0:
            errorMessages += "<li>WAS_HOME is not set</li>"
            error = True
        if len(profileParameters['host']) <= 0:
            errorMessages += "<li>Host is not set</li>"
            error = True
        if len(profileParameters['port']) <= 0:
            errorMessages += "<li>Port is not set</li>"
            error = True
        if len(profileParameters['conntype']) <= 0:
            errorMessages += "<li>Connection type is not set</li>"
            error = True
        if len(profileParameters['username']) <= 0:
            errorMessages += "<li>Username type is not set</li>"
            error = True
        if len(profileParameters['password']) <= 0:
            errorMessages += "<li>Password type is not set</li>"
            error = True
        if error:
            QtGui.QMessageBox.warning(self, "Fields not set", errorMessages)

        return error

    def updateProfileAction(self):
        pass

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def profileName(self):
        return self.profileNameInput.text

    @profileName.setter
    def profileName(self, profileName):
        self.profileNameInput.setText(QtCore.QString(profileName))