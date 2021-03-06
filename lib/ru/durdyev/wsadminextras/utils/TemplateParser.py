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

# parse scripts and replace parameters
class TemplateParser(object):

    # path to templates scripts directory
    _template_dir = "../scripts/templates/"

    # template files extension
    _template_ext = ".template"

    _replace_parameters = {
        'application_path' : '%application_path%'
    }

    def generateScriptFromTemplate(self, scriptName, params, profile):
        try:
            fileContent = None
            if  os.path.exists(self.template_dir):
                fileContent = self.getFileContent(scriptName + self.template_ext)
                for parameter in params:
                    if parameter in self.replace_parameters:
                        if parameter == 'application_path':
                            replace_param = "../profiles/" + profile + "/tmp/" + params[parameter]
                            fileContent = fileContent.replace(self.replace_parameters[parameter], replace_param)
                    else:
                        replace_param = params[parameter]
                        fileContent = fileContent.replace("%" + parameter + "%", replace_param)
                return fileContent+'\n'
        except IOError as e:
            print("Cant't read template file from scripts. See logs.")
            logging.error(e.message)

    def getFileContent(self, fileName):
        if os.path.exists(self.template_dir):
            filePath = self.template_dir + fileName
            file = open(filePath)
            return file.read()

        return ""

    @property
    def template_dir(self):
        return self._template_dir

    @property
    def template_ext(self):
        return self._template_ext

    @property
    def replace_parameters(self):
        return self._replace_parameters