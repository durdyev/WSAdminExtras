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

import os
import logging

LOGGING_FOLDER = '../logs'
LOGGING_FILE = LOGGING_FOLDER + '/log.out'

#if log folder doesnt exists then create log folder.
def create_log_folder():
    try:
        os.mkdir(LOGGING_FOLDER)
        print('logging folder create successfully!')
        return True
    except OSError as e:
        print('Cannot create a folder. Maybe folder is exists. Check it.')
        return False

#configure logger system
def configure_logging():
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(name)s::%(message)s',
        dateformat='%m/%d/%Y %I:%M:%S %p',
        filename=LOGGING_FILE,
        level=logging.INFO
    )
