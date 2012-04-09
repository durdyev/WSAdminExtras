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

class ProfileWidget(QtGui.QWidget):

    _profileName = None

    def __init__(self, parent, profileName):
        super(ProfileWidget, self).__init__(parent)
        self._profileName = profileName
        self.initUI()
        self.initProfileSettings()

    def initUI(self):
        self.qTabWidget = QtGui.QTabWidget(self)
        self.qTabBar = QtGui.QTabBar(self.qTabWidget)
        self.qTabWidget.setGeometry(0, 0, 343, 220)

        self.qSettingsTab = QtGui.QWidget(self.qTabWidget)
        self.qSettingsGridLayout = QtGui.QGridLayout()
        self.qSettingsTab.setLayout(self.qSettingsGridLayout)

        self.qFilesTab = QtGui.QWidget(self.qTabWidget)
        self.qFilesGridLayout = QtGui.QGridLayout()
        self.qFilesTab.setLayout(self.qFilesGridLayout)

        self.qTabWidget.addTab(self.qSettingsTab, "Settings")
        self.qTabWidget.addTab(self.qFilesTab, "Files")

    def initProfileSettings(self):
        # was home
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("WAS_HOME")), 0, 0)
        wasHomeInput = QtGui.QLineEdit()
        self.qSettingsGridLayout.addWidget(wasHomeInput, 0, 1)

        # host
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Host")), 1, 0)
        hostInput = QtGui.QLineEdit()
        self.qSettingsGridLayout.addWidget(hostInput, 1, 1)

        # port
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Port")), 2, 0)
        portInput = QtGui.QLineEdit()
        self.qSettingsGridLayout.addWidget(portInput, 2, 1)

        # connection type
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Connection type")), 3, 0)
        connTypeInput = QtGui.QLineEdit()
        self.qSettingsGridLayout.addWidget(connTypeInput, 3, 1)

        # admin user
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Admin user")), 4, 0)
        adminUserInput = QtGui.QLineEdit()
        self.qSettingsGridLayout.addWidget(adminUserInput, 4, 1)

        # password
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Password")), 5, 0)
        passwordInput = QtGui.QLineEdit()
        self.qSettingsGridLayout.addWidget(passwordInput, 5, 1)

        ## buttons
        # update button
        updateProfileButton = QtGui.QPushButton("Update profile")
        self.qSettingsGridLayout.addWidget(updateProfileButton, 6,0)

        ## buttons
        # update button
        deleteProfileButton = QtGui.QPushButton("Delete profile")
        self.qSettingsGridLayout.addWidget(deleteProfileButton, 6,1)