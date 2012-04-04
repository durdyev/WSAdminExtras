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
from ru.durdyev.wsadminextras.ui.server.CreateProfileWidget import CreateProfileWidget
from ru.durdyev.wsadminextras.utils.ProfileUtils import ProfileUtils
from ru.durdyev.wsadminextras.ui.utils.WidgetModes import WidgetModes

## Server UI
class ServerApplication(QtGui.QMainWindow):

    # application title
    _server_application_title = 'WSAdminExtras Server'

    # application width
    _app_width = 500

    # application height
    _app_height = 220

    #base profiler
    _base_profiler = ProfileUtils()

    #widget modes
    _widget_modes = WidgetModes()

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
        qBaseWidget = QtGui.QWidget(self)
        qBaseWidgetLayout = QtGui.QGridLayout()
        qBaseWidget.setLayout(qBaseWidgetLayout)
        qBaseWidget.setGeometry(0,20,150,200)

        # tree view
        qTreeView = QtGui.QTreeView(qBaseWidget)
        qTreeView.setGeometry(0,0,150,200)

        # main tree
        qTree = QtGui.QTreeWidget(qBaseWidget)
        qTree.setGeometry(0,0,150,200)

        # top level elements
        qServerElement = QtGui.QTreeWidgetItem(['Server'])
        qProfilesElement = QtGui.QTreeWidgetItem(['Profiles'])

        # server elements
        qServerElement.addChild(QtGui.QTreeWidgetItem(['Status']))
        qServerElement.addChild(QtGui.QTreeWidgetItem(['Settings']))

        #profiles elements
        profiles = self._base_profiler.get_profile_list()
        for profile in profiles:
            profileItem = QtGui.QTreeWidgetItem([profile])
            qProfilesElement.addChild(profileItem)

        qTree.addTopLevelItems([qServerElement, qProfilesElement])

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