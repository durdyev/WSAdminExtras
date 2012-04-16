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

from PyQt4 import QtGui
from PyQt4 import QtCore

from lib.ru.durdyev.wsadminextras.server.BaseProfiler import BaseProfiler

class ProfileWidget(QtGui.QWidget):

    _profileName = None

    _baseProfiler = BaseProfiler()

    def __init__(self, parent, profileName):
        super(ProfileWidget, self).__init__(parent)
        self._profileName = profileName
        self.initUI()
        self.initProfileSettingsTab()
        self.initProfileFilesTab()

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

    def initProfileSettingsTab(self):
        # was home
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("WAS_HOME")), 0, 0)
        wasHome = QtCore.QString(self._baseProfiler.get_was_home(self._profileName))
        self.wasHomeInput = QtGui.QLineEdit(wasHome)
        self.qSettingsGridLayout.addWidget(self.wasHomeInput, 0, 1)

        # host
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Host")), 1, 0)
        host = QtCore.QString(self._baseProfiler.get_host(self._profileName))
        self.hostInput = QtGui.QLineEdit(host)
        self.qSettingsGridLayout.addWidget(self.hostInput, 1, 1)

        # port
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Port")), 2, 0)
        port = QtCore.QString(self._baseProfiler.get_port(self._profileName))
        self.portInput = QtGui.QLineEdit(port)
        self.qSettingsGridLayout.addWidget(self.portInput, 2, 1)

        # connection type
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Connection type")), 3, 0)
        conntype = QtCore.QString(self._baseProfiler.get_conntype(self._profileName))
        self.connTypeInput = QtGui.QLineEdit(conntype)
        self.qSettingsGridLayout.addWidget(self.connTypeInput, 3, 1)

        # admin user
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Admin user")), 4, 0)
        adminUser = QtCore.QString(self._baseProfiler.get_username(self._profileName))
        self.adminUserInput = QtGui.QLineEdit(adminUser)
        self.qSettingsGridLayout.addWidget(self.adminUserInput, 4, 1)

        # password
        self.qSettingsGridLayout.addWidget(QtGui.QLabel(QtCore.QString("Password")), 5, 0)
        password = QtCore.QString(self._baseProfiler.get_password(self._profileName))
        self.passwordInput = QtGui.QLineEdit(password)
        self.qSettingsGridLayout.addWidget(self.passwordInput, 5, 1)

        ## buttons
        # update button
        updateProfileButton = QtGui.QPushButton("Update profile")
        updateProfileButton.clicked.connect(self.updateProfile)
        self.qSettingsGridLayout.addWidget(updateProfileButton, 6,0)

        ## buttons
        # update button
        deleteProfileButton = QtGui.QPushButton("Delete profile")
        self.qSettingsGridLayout.addWidget(deleteProfileButton, 6,1)

    def initProfileFilesTab(self):
        self.qFilesTreeView = QtGui.QTreeView()
        self.qFileTreeList = QtGui.QTreeWidget(self.qFilesTreeView)
        self.qFileTreeList.setGeometry(0, 0, 326, 155)
        self.qFileTreeList.setHeaderLabels(['Name', 'Type', 'Size'])

        self.qFilesGridLayout.addWidget(self.qFilesTreeView, 0, 0)

        for item in self._baseProfiler.get_file_list(self._profileName):
            name = str(item['name'])
            type = str(item['type'])
            size = str(item['size'])

            self.qFileTreeList.addTopLevelItem(QtGui.QTreeWidgetItem([name, type, size]))

        # buttons
        self.deleteFileButton = QtGui.QPushButton("Delete file")
        self.deleteFileButton.clicked.connect(self.confirmFileDelete)
        self.qFilesGridLayout.addWidget(self.deleteFileButton)

    def clearProfileFilesTab(self):
        for i in range(self.qFilesGridLayout.count()):
            self.qFilesGridLayout.itemAt(i).widget().close()

    def updateProfile(self):
        params = {
            'was_home' : str(self.wasHomeInput.text()),
            'host' : str(self.hostInput.text()),
            'port' : str(self.portInput.text()),
            'conntype' : str(self.connTypeInput.text()),
            'username' : str(self.adminUserInput.text()),
            'password' : str(self.passwordInput.text())
        }
        if (self._baseProfiler.update_configuration_file(self._profileName, params) != 0):
            QtGui.QMessageBox.warning(self, QtCore.QString("Error"),
                QtCore.QString("Can't update profile config. See logs."))

        QtGui.QMessageBox.information(self, QtCore.QString("Message"),
            QtCore.QString("Profile configuration successfully updated."))

    def confirmFileDelete(self):
        dialog = QtGui.QDialog(self)
        dialog.show()

    def deleteSelectedFile(self):
        for item in self.qFileTreeList.selectedItems():
            fileName = item.text(0)
            filePath = self._baseProfiler.get_tmp_dir(self._profileName) + "/" + fileName
            os.remove(filePath)

            self.clearProfileFilesTab()
            self.initProfileFilesTab()