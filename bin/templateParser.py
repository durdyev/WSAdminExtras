# TODO delete this file after review

import sys
sys.path.append("../lib")

from ru.durdyev.wsadminextras.utils.TemplateParser import TemplateParser

params = {
    "app_name" : "simple.ear",
    "node_name" : "simplenode",
    "server_name" : "server1"
}
templateParser = TemplateParser()
print(templateParser.generateScriptFromTemplate("deploy", params))