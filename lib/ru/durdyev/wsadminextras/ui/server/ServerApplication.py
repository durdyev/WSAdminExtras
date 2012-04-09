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
        self.qServerElement.addChild(QtGui.QTreeWidgetItem(['Status']))
        self.qServerElement.addChild(QtGui.QTreeWidgetItem(['Settings']))

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

    def newProfileActionSlot(self):
        message = 'Trying to create new profile'

        # creating new profile
        createProfileWidget = CreateProfileWidget(self, WidgetModes.create_mode)
        self.connect(createProfileWidget, QtCore.SIGNAL("profileCreated(QString)"),
            self.profileCreatedSlot)

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

    def initProfileSelectedTabBar(self, profileName):
        if self._profileWidget is not None:
            self._profileWidget.hide()

        self._profileWidget = ProfileWidget(self, profileName)
        self._profileWidget.setObjectName(profileName)
        self.qRightWidgetGrid.addWidget(self._profileWidget, 0, 0)