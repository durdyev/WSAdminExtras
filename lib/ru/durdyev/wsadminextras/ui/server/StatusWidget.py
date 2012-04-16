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

class StatusWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        super(StatusWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.statusWidgetGridLayout = QtGui.QGridLayout()
        self.statusWidget = QtGui.QWidget(self)
        self.statusWidget.setLayout(self.statusWidgetGridLayout)
        self.statusWidget.setGeometry(0, 0, 345, 150)

        self.topGridLayout = QtGui.QGridLayout()
        self.bottomGridLayout = QtGui.QGridLayout()

        self.topWidget = QtGui.QWidget()
        self.topWidget.setLayout(self.topGridLayout)

        self.bottomWidget = QtGui.QWidget()
        self.bottomWidget.setLayout(self.bottomGridLayout)

        self.statusWidgetGridLayout.addWidget(self.topWidget, 0, 0)
        self.statusWidgetGridLayout.addWidget(self.bottomWidget, 1, 0)

        statusLabel = QtGui.QLabel("Server started")
        statusLabel.setStyleSheet("font-size:40px;text-align:center")
        self.topGridLayout.addWidget(statusLabel, 0, 0)

        self.startButton = QtGui.QPushButton("Start server")
        self.bottomGridLayout.addWidget(self.startButton, 1, 0)

        self.stopButton = QtGui.QPushButton("Stop server")
        self.bottomGridLayout.addWidget(self.stopButton, 1, 1)