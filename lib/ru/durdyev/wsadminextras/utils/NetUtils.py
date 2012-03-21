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

import random, time
import md5

# net utilities.
class NetUtils(object):
    #generate request id for conversation
    @staticmethod
    def generate_request_id():
        return md5.new(str(random.random()) + str(time.ctime())).digest()

    #return request delimeter n
    @staticmethod
    def delimeter_n():
        return '\n'

    #return request delimeter rn
    @staticmethod
    def delimeter_rn():
        return '\r\n'
