'''
Created on 13/03/2014

@author: MMPE
'''
from __future__ import division, absolute_import, unicode_literals

import os
import sys
import inspect

if sys.executable.lower().endswith("controller.exe"):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.relpath(os.path.join(os.path.dirname(__file__), "../../")))

from ui.qt_ui import QtUI
from ui.scripting_window.ScriptRunner import ScriptRunner
from ui.scripting_window.ScriptingWindow import ScriptingWindow, \
    ScriptingMainWindow
from ui.scripting_window.script_function import script_function_class_list


try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

#class Gui(ScriptingWindow, QtUI):
#    def __init__(self, controller, model):
#        ScriptingWindow.__init__(self, controller, model, self)
#        QtUI.__init__(self, self)

class ScriptingWindowController(object):
    def __init__(self):

        if sys.executable.lower().endswith("controller.exe"):
            self.function_docs = """docs/ScriptFunctions.html"""
        else:
            self.function_docs = """ui/scripting_window/docs/ScriptFunctions.html"""


        self.model = None
        self.gui = ScriptingMainWindow(self, self.model)

        self.application_name = "ScriptingFunctionWindow"
        self.load_script_functions(self.gui, self.model, "ui/scripting_window/appfuncs")
        self.load_script_functions(self.gui, self.model, "appfuncs")
        self.scriptRunner = ScriptRunner(self, self.gui, None)
        self.gui.start()

    def load_script_functions(self, gui, model, root_path):
        if not hasattr(self, 'appFuncs'):
            self.appFuncs = []
        for func_cls in script_function_class_list(root_path):
            func_obj = func_cls(self, gui, model)
            self.appFuncs.append(func_obj)
            setattr(self, func_obj.class_name, func_obj)

if __name__ == "__main__":
    controller = ScriptingWindowController()
    os._exit(0)  #ensure termination
