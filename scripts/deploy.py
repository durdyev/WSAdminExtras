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

import sys

# the list of depployable applications
execfile('wsadminlib.py')

temp_dir_path = '../tmp'

def main():
    if (len(sys.argv) <= 2):
        print('Parameters is not set.')
        return
    else:
        try:
            application_path = sys.argv[1]
            application_name = sys.argv[2]
            parameters = sys.argv[3]
            if sys.argv[4] is not None:
                parameters += sys.argv[4]

        except IndexError:
            print("parameters not set")

    if sys.argv[0] == 'INSTALL':
        install(application_path, parameters)
        saveAndSync()
        start(application_name)
    if sys.argv[0] == 'UNINSTALL':
        uninstall(application_name)
        saveAndSync()

def install(application_path, parameters):
    AdminApp.install(application_path, parameters)

def uninstall(application_name):
    AdminApp.uninstall(application_name)

def start(application_name):
    startApplication(application_name)

if __name__== '__main__':
    main()