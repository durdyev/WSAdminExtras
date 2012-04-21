## TODO delete this file after review
#
#import sys
#sys.path.append("../lib")
#
#from ru.durdyev.wsadminextras.utils.TemplateParser import TemplateParser
#
#params = {
#    "app_name" : "simple.ear",
#    "node_name" : "simplenode",
#    "server_name" : "server1"
#}
#templateParser = TemplateParser()
#print(templateParser.generateScriptFromTemplate("deploy", params))

import re

str = "{ [node:node1], [server:server], [appname:loan] }"

def parseParameters(parameterStr):
    parameters_dict = {}
    if parameterStr is not None:
        regexp_params = re.findall("\[([aA-zZ0-9]+\:[aA-zZ0-9]+)\]", parameterStr)
        if regexp_params is not None:
            for p in regexp_params:
                param_regexp = re.search("([aA-zZ0-9]+)\:([aA-zZ0-9]+)", p)
                if param_regexp is not None:
                    parameters_dict[param_regexp.group(1)] = param_regexp.group(2)
    return parameters_dict

print(parseParameters(str))