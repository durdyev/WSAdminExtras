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

import logging
import os

from xml.dom.minidom import Document

# profile manager class
# @author idurdyev

class BaseProfiler(object):
    #profile directory
    _profile_dir = '../profiles/'
    #config directory
    _profile_config_dir = _profile_dir + '/config'
    #tmp directory
    _profile_temp_dir = _profile_dir + '/tmp'

    def __init__(self, profile_name):
        self.create_profile(profile_name)
        self.create_configuration_files(profile_name)

    def create_profile(self, profile_name):
        if profile_name is not None:
            logging.info('BaseProfiler.create_profile.'
            + 'Trying to create profile with name \'%s\'' % profile_name)
            try:
                self._profile_dir += profile_name
                os.makedirs(self._profile_dir)
                os.makedirs(self._profile_config_dir)
                os.makedirs(self._profile_temp_dir)
            except OSError as e:
                logging.warn('Error. profile with name %s is exists' % profile_name)
                print('Can\'t create profile. Profile with same name is exists.',\
                      'Try to create profile with another name')

    def create_configuration_files(self, profile_name):
        doc = Document()