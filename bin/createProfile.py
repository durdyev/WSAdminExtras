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

# crating a profile for the server
# @author idurdyev

import sys

sys.path.append("../lib")
import  logging
import baseFunc
from xml.dom.minidom import Document

#ru.durdyev.* packages and classes
from ru.durdyev.wsadminextras.server import BaseProfiler

#main method, entry point
def main():
    #creating log folder if not exist
    try:
        baseFunc.configure_logging()
        logging.info('Creating profile')
    except IOError as e:
        print('logging folder doesn\'t exist')
        print('trying to create logging folder...')
        if baseFunc.create_log_folder():
            baseFunc.configure_logging()

    if len(sys.argv) > 2:
        arg_names = ['filename', 'key', 'argument']
        arguments = dict(zip(arg_names, sys.argv))
        if arguments['key'] == '-profileName':
            create_new_profile(arguments['argument'])
    else:
        print('Incorrect usage')

#create new profile	
def create_new_profile(profileName):
    BaseProfiler.BaseProfiler(profileName)

if __name__ == '__main__':
    main()
