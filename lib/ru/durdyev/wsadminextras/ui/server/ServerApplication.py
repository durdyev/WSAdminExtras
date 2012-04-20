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
from ru.durdyev.wsadminextras.ui.server.CreateProfileWidget import CreateProfileWidget
from ru.durdyev.wsadminextras.utils.ProfileUtils import ProfileUtils
from ru.durdyev.wsadminextras.ui.utils.WidgetModes import WidgetModes
from ru.durdyev.wsadminextras.ui.server.ProfileWidget import ProfileWidget
from ru.durdyev.wsadminextras.ui.server.ServerSettingsWidget import ServerSettingsWidget
from ru.durdyev.wsadminextras.ui.server.StatusWidget import StatusWidget
from ru.durdyev.wsadminextras.server.ServerManager import ServerManager
from ru.durdyev.wsadminextras.server.BaseWSAdminExtrasServer import BaseWSAdminExtrasServer
from ru.durdyev.wsadminextras.server.RequestEventHandler import RequestEventHandler
from ru.durdyev.wsadminextras.utils.ServerSettings import ServerSettings
from ru.durdyev.wsadminextras.utils.ServerCodes import ServerCodes

## Server UI
class ServerApplication(QtGui.QMainWindow):

    # application title
    _server_application_title = 'WSAdminExtras Server'

    # application width
    _app_width = 500

    # application height
    _app_height = 250

    #base profiler
    _base_profiler = ProfileUtils()

    #widget modes
    _widget_modes = WidgetModes()

    # profiles tree item text
    _profilesItemText = "Profiles"

    # settings tree item text
    _settingsItemText = "Settings"

    # status tree item text
    _statusItemText = "Status"

    # profile widget
    _profileWidget = None

    def __init__(self):
        super(ServerApplication, self).__init__()
        self.initUI()

    ## Initialize UI
    def initUI(self):
        self.setGeometry(300, 200, self._app_width, self._app_height)
        self.setWindowTitle(self._server_application_title)
        self.initMenuBar()
        self.initBaseUI()
        self.show()

    def initMenuBar(self):
        # initialize menubar
        menuBar = self.menuBar()

        # file menu
        fileMenu = menuBar.addMenu('&File')
        # file > create profile
        fileMenu.addAction(self.newProfileAction)

        # view menu
        viewMenu = menuBar.addMenu('&View')
        # view > logs
        viewMenu.addAction(self.viewLogsAction)

        # exit action
        menuBar.addAction(self.exitAction)

    def initBaseUI(self):
        # base widget
        self.qBaseWidget = QtGui.QWidget(self)
        self.qBaseWidget.setGeometry(0, 20, self._app_width, self._app_height)

        # left widget layout
        self.qLeftWidgetGrid = QtGui.QGridLayout()
        self.qLeftWidgetLayout = QtGui.QWidget(self.qBaseWidget)
        self.qLeftWidgetLayout.setLayout(self.qLeftWidgetGrid)
        self.qLeftWidgetLayout.setGeometry(0,0,150,230)

        # right widget layout
        self.qRightWidgetGrid = QtGui.QGridLayout()
        self.qRightWidgetLayout = QtGui.QWidget(self.qBaseWidget)
        self.qRightWidgetLayout.setLayout(self.qRightWidgetGrid)
        self.qRightWidgetLayout.setGeometry(140, 0, 350, 230)
        # tree view
        self.qTreeView = QtGui.QTreeView()
        self.qTreeView.setGeometry(0,0,150,230)
        self.qLeftWidgetGrid.addWidget(self.qTreeView, 0, 0)

        # main tree
        self.qTree = QtGui.QTreeWidget(self.qTreeView)
        self.qTree.setGeometry(0,0,141,220)
        self.qTree.setStyleSheet("padding-left:2px")
        self.qTree.clicked.connect(self.clickToTree)

        self.initTree()

    def initTree(self):
        # top level elements
        self.qServerElement = QtGui.QTreeWidgetItem([self._settingsItemText])
        self.qProfilesElement = QtGui.QTreeWidgetItem([self._profilesItemText])

        # server elements
        self.qServerElement.addChild(QtGui.QTreeWidgetItem([self._statusItemText]))
        self.qServerElement.addChild(QtGui.QTreeWidgetItem([self._settingsItemText]))

        #profiles elements
        profiles = self._base_profiler.get_profile_list()
        for profile in profiles:
            profileItem = QtGui.QTreeWidgetItem([profile])
            self.qProfilesElement.addChild(profileItem)

        self.qTree.addTopLevelItems([self.qServerElement, self.qProfilesElement])

    # exit action
    @property
    def exitAction(self):
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(QtGui.qApp.quit)

        return exitAction

    # new profile action
    @property
    def newProfileAction(self):
        newProfileAction = QtGui.QAction('&New Profile', self)
        newProfileAction.triggered.connect(self.newProfileActionSlot)

        return newProfileAction

    # view logs action
    @property
    def viewLogsAction(self):
        viewLogsAction = QtGui.QAction('&Logs', self)
        viewLogsAction.triggered.connect(self.viewLogsActionSlot)

        return viewLogsAction

    def newProfileActionSlot(self):
        message = 'Trying to create new profile'

        # creating new profile
        createProfileWidget = CreateProfileWidget(self, WidgetModes.create_mode)
        self.connect(createProfileWidget, QtCore.SIGNAL("profileCreated(QString)"),
            self.profileCreatedSlot)

    def viewLogsActionSlot(self):
        print("View logs")

    def profileCreatedSlot(self, profile):
        print("profile created %s" % profile)
        self.qTree.clear()
        self.initTree()

    def clickToTree(self):
        currentItem = self.qTree.currentItem()
        parentItem = currentItem.parent()

        if parentItem is not None:
            if parentItem.text(0) == self._profilesItemText:
                profileNameSelected = currentItem.text(0)
                self.initProfileSelectedTabBar(profileNameSelected)
            if parentItem.text(0) == self._settingsItemText:
                if currentItem.text(0) == self._settingsItemText:
                    self.initSettings()
                if currentItem.text(0) == self._statusItemText:
                    self.initStatus()

    def initStatus(self):
        self.clearRightGridLayout()

        self.statusWidget = StatusWidget()
        self.qRightWidgetGrid.addWidget(self.statusWidget, 0, 0)

    def initSettings(self):
        self.clearRightGridLayout()

        serverSettingsWidget = ServerSettingsWidget()
        self.qRightWidgetGrid.addWidget(serverSettingsWidget, 0, 0)

    def initProfileSelectedTabBar(self, profileName):
        self.clearRightGridLayout()

        if self._profileWidget is not None:
            self._profileWidget.hide()

        self._profileWidget = ProfileWidget(self, profileName)
        self._profileWidget.setObjectName(profileName)
        self.qRightWidgetGrid.addWidget(self._profileWidget, 0, 0)

    def clearRightGridLayout(self):
        for i in range(self.qRightWidgetGrid.count()):
            self.qRightWidgetGrid.itemAt(i).widget().close()