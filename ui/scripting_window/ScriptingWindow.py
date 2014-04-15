from __future__ import division, absolute_import, unicode_literals, print_function
from build_exe import exe_std_out
from build_exe.exe_std_out import ExeStdOut
from QtGuiLoader.QtGuiLoader import QtMainWindowLoader
from ui.qt_ui import QtUI
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

from multiprocessing.process import Process
import os
import re
import sys
from ui.scripting_window.script_function import ScriptFunction
import inspect


import time
import traceback
import MyQt
from MyQt.QtWebKit import QWebPage
from MyQt.QtCore import Qt, QUrl
from MyQt.QtGui import QMessageBox, QDialog, QFileDialog, QIcon, QApplication
from QtGuiLoader import QtDialogLoader
from datastructures.Singleton import singleton
from ui.scripting_window import ScriptingWindowUI
from ui.scripting_window.ScriptRunner import ScriptRunner
from ui.scripting_window.ScriptTab import ScriptTab
from ui.text_ui import TextUI


def beep(frq=2500, dur=50):
    if sys.platform == 'win32':
        import winsound
        winsound.Beep(frq, dur)





class ScriptingWindow(object):

    autosave_splitter = """
#===============================================================================
# Autosave
#===============================================================================
"""

    autosave_filename = "autosave.py"
    handle_focus = False
    anchor = None

    def __init__(self, controller, gui, model, appfuncs_path="appfuncs"):
        self.font_size = 10
        self.controller = controller
        self.model = model
        self.gui = gui
        self.appfuncs_path = appfuncs_path

        self.load_autosave()
        self.ui.splitter.setSizes([400, 200])
        self.ui.splitter_2.setSizes([800, 400])

        # self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui.tabWidget.setFocusPolicy(Qt.StrongFocus)
        self.ui.tabWidget.focusInEvent = self.focusInEvent
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)
        self.setWindowIcon(QIcon('graphics/Pdap.ico'))



        self.ui.webView.loadFinished.connect(self.documentation_load_finished)
        #self.ui.webView.linkClicked.connect(self.linkclicked)
        #self.ui.webView.loadStarted.connect(self.loadstarted)
        self.doc_path = os.path.join("docs/")

        with open(self.doc_path + 'doc.html') as fid:
            self.method_doc_template = fid.read()
        with open(self.doc_path + 'source.html') as fid:
            self.method_source_template = fid.read()


        self.ui.webView.setUrl(QUrl(self.doc_path + "index.html"))


    def tab_changed(self, index):
        pass

    def linkclicked(self, url="none"):
        print ("linkclicked", url)


    def loadstarted(self):
        print ("load start", self.ui.webView.url())

    @property
    def scriptRunner(self):
        return self.controller.scriptRunner

    def show_documentation(self, obj):
        #cls = obj.im_class
        #module = obj.im_class.__module__
        if obj.__name__ == "run" and issubclass(obj.im_class, ScriptFunction):
            obj = obj.im_self

        if isinstance(obj, ScriptFunction):
            html = self.method_doc_template
            func_path = os.path.relpath(inspect.getabsfile(obj.__class__), os.getcwd())
            module_name = os.path.splitext(func_path)[0].replace(os.path.sep, ".")
            self.ui.webView.setUrl(QUrl(os.path.join(self.doc_path, "doc.html?#%s.%s.run" % (module_name, obj.class_name))))

    def html_source(self):
        return self.ui.webView.page().mainFrame().toHtml()

    @property
    def doc_contents(self):
        return self.ui.webView.page().mainFrame().findFirstElement("div.contents").toInnerXml()

    @doc_contents.setter
    def doc_contents(self, html):
        return self.ui.webView.page().mainFrame().findFirstElement("div.contents").setInnerXml(html)



    def documentation_load_finished(self, ok):
        url = self.ui.webView.url()
        url_path = str(url.path())
        url_fragment = str(url.fragment()).replace('library.zip.appfuncs.', 'appfuncs.')
        ExeStdOut(url_path, url_fragment)
        #print (url_path)
        #print (url_fragment)
        if url_path.endswith("docs/doc.html"):
            #print (self.controller.function_docs, os.path.isfile(self.controller.function_docs))
            with open(self.controller.function_docs) as fid:
                doc_html = str(fid.read(), 'utf-8')

            if not url_fragment.endswith(".run"):
                url_fragment += ".run"


            start_tag = '<dt id="%s">' % url_fragment
            end_tag = '</dd>'

            scriptFunction_name = url_fragment.split(".")[-2]
            try:
                method_html = start_tag + doc_html.split(start_tag)[1].split(end_tag)[0] + end_tag
                for a, b in [('<tt class="descname">run</tt>', '<tt class="descname">%s</tt>' % scriptFunction_name),
                    ('href="_modules', 'href="source.html?#_modules'),
                    ("Parameters :", "Parameters:"),
                    ("Return :", "Return:"),
                    ]:
                    method_html = method_html.replace(a, b)
            except IndexError:
                method_html = "Documentation not found"
            self.doc_contents = method_html




        elif url_path.endswith("docs/source.html"):
            source_html_path, self.anchor = str(url.fragment()).split("#")

            with open("%s/%s" % (os.path.dirname(self.controller.function_docs), source_html_path)) as fid:
                source_html = str(fid.read(), 'utf-8')
            source_html = source_html.replace('<a class="viewcode-back" href="../../../ScriptFunctions.html', '<a class="viewcode-back" href="doc.html')
            #print (source_html)

            p = QWebPage()
            f = p.mainFrame()
            f.setHtml(source_html)
            self.doc_contents = f.findFirstElement('div.body').toInnerXml()


        if self.anchor:
            self.ui.webView.page().mainFrame().scrollToAnchor(self.anchor)
        with open(self.doc_path + "tmp.html", 'w') as fid:
            fid.write(self.html_source())


    def focusInEvent(self, event):
        if self.handle_focus:
            self.handle_focus = False
            tab = self.ui.tabWidget.currentWidget()
            if tab is not None and tab.is_modified():
                msg = 'The file \'%s\' has been changed on the file system. Do you want to replace the editor contents with these changes?' % tab.filename
                msg += "\n\n" + "\n".join(["Diff in line %d:\nIn script: %s\nIn file:   %s\n" % (lnr, l1, l2) for lnr, (l1, l2) in enumerate(zip(tab.get_script().split("\n"), tab.saved().split("\n"))) if l1.strip() != l2.strip()][:5])
                if QMessageBox.information(self, 'File changed', msg, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    tab.reload()
                else:
                    tab.filemodified = os.path.getmtime(tab.filename)
            self.handle_focus = True

    def autosave(self):
        s = []
        for i in range(self.ui.tabWidget.count()):
            tab = self.ui.tabWidget.widget(i)
            s.append("%s#%s\n#%s\n%s" % (self.autosave_splitter, tab.filename, tab.filemodified, tab.get_script()))

        with open(self.autosave_filename, 'w') as fid:
            fid.write("".join(s))

    def load_autosave(self):

        autosave = self._load_script(self.autosave_filename)
        scripts = autosave.split(self.autosave_splitter)
        for s in scripts[1:]:
            filename = s.splitlines()[0][1:]
            filemodified = float(s.splitlines()[1][1:])
            script = "\n".join(s.splitlines()[2:])
            tab = self._actionNew(filename, script, filemodified)
            #tab.dirty = not tab.equals_saved()
        if self.ui.tabWidget.count() == 0:
            self._actionNew()

    def close(self):
        self.autosave()


    def _actionNew(self, filename="New", script="", filemodified=0):
        tab = ScriptTab(self, filename, script, filemodified)
        self.ui.tabWidget.addTab(tab, tab.title)
        tab.filename_changed()
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)
        return tab

    def _actionRunScript(self):
        self.autosave()
        script = self.ui.tabWidget.currentWidget().get_script()
        self.run_script(script)

    def run_script(self, script):
        self.gui.start_wait()
        self.set_output("")
        self.ui.labelLineNumber.setText("")
        QApplication.processEvents()
        sys.stdout = self
        starttime = -time.clock()

        try:

            self.output = []
            self.scriptRunner.run(script)

        except (Warning, Exception) as inst:
            traceback.print_exc(file=sys.stdout)
            sys.stdout = sys.__stdout__
            try:
                linenr = self.output[[self.output.index(l) for l in self.output if "File \"<string>\", line " in l][-1]]
                linenr = linenr[23:]
                if "," in linenr:
                    linenr = int(linenr[:linenr.index(",")])
                else:
                    linenr = int(linenr)

                self.selectLine(linenr - 1)
            except IndexError:
                pass
            print ('-' * 60)
            beep(500, 50)
        finally:

            sys.stdout = sys.__stdout__
        self.ui.labelLineNumber.setText("Script executed in %d seconds" % (time.clock() + starttime))
        self.gui.end_wait()

    def write(self, s):
        try:
            sys.__stdout__.write(s)
        except IOError:
            #flush not working in no console cx_freeze application
            pass
        self.output.append(s)
        self.set_output("".join(self.output))


    def flush(self):
        pass  # solves problem on linux

    def selectLine(self, linenr):
        self.ui.tabWidget.currentWidget().editor.setSelection(linenr, 0, linenr, -1)
#        te = self.ui.tabWidget.currentWidget().textEditScript
#
#        cur_line = te.textCursor().blockNumber()
#        diff = linenr - cur_line
#        move = QTextCursor.Down if diff >= 0 else QTextCursor.Up
#        for _ in range(abs(diff)): te.moveCursor(move, QTextCursor.MoveAnchor)
#        te.moveCursor(QTextCursor.StartOfLine,0)
#        te.moveCursor(QTextCursor.EndOfLine,QTextCursor.KeepAnchor)

    def _exec(self, script):
        exec(script)

    def updateElapsed(self):
        self.elapsed += 1
        print (self.elapsed)
        self.ui.labelLineNumber.setText("Elapsed: %d" % self.elapsed)

    def close_tab(self, index):
        self.ui.tabWidget.setCurrentIndex(index)
        self.ui.tabWidget.widget(index).close()
        if self.ui.tabWidget.count() == 0:
            self._actionNew()

    def _actionOpen(self, filename=""):
        if filename == "":
            filename = str(QFileDialog.getOpenFileName(self, "Open script", "./scripts", "*.py"))
            if filename == '':
                return
        if os.path.isfile(filename):
            self._actionNew(filename, self._load_script(filename), os.path.getmtime(filename))

    def _actionSave(self):
        tab = self.ui.tabWidget.currentWidget()
        if os.path.isfile(tab.filename):
            tab._save()
        else:
            self._actionSaveAs()

    def _actionSaveAs(self):
        filename = str(QFileDialog.getSaveFileName(self, "Save script", "./scripts", "*.py"))
        if filename != "":
            self.ui.tabWidget.currentWidget().filename = filename
            try:
                f = open(filename, 'w')
                f.close()
            except:
                pass
            self._actionSave()

    def _actionImportPlugin(self, plugin_filename=None):
        self.close()
        if plugin_filename is None:
            plugin_filename = str(QFileDialog.getOpenFileName(self, "Open plugin file", "./plugins", "*.py"))
        if os.path.isfile(plugin_filename):
            f = open(plugin_filename)
            plugin = f.read()
            f.close()

            def is_plugin(plugin):
                return re.compile('class [\w ]*\([\w, ]*Plugin[\w, ]*\):[^\b]*def run\(self\):\n        ').search(plugin)

            r = is_plugin(plugin)
            if r is None:

                QMessageBox.warning(self, "Import error", "Script in \n\n%s\n\ncould not be identified as a plugin" % plugin_filename, QMessageBox.Ok)
            else:
                script = plugin[r.end():].replace("\n        ", "\n")
                self.set_script(script)

    def _actionExportPlugin(self):
        global plugin_name, plugin_menu_pos
        tab = self.ui.tabWidget.currentWidget()
        if tab.filename == "":
            plugin_name = "my_plugin"
        else:
            plugin_name = os.path.basename(tab.filename).replace(".py", "")

        from gui.InputParameters import PluginParameters
        param = PluginParameters()
        param._items[0]._default = plugin_name
        param._items[1]._default = "[\"Plugins\"]"
        param.set_defaults()
        if not param.edit():
            return None
        plugin_name = param.name.replace(" ", "_")
        plugin_text = param.name
        menu_pos = param.window_menu_pos
        if plugin_name in dir(self):
            if not self.gui.confirm("Confirm export", "The plugin '%s' already exists\nDo you want to replace it" % plugin_name):
                return

        #plugin_filename = str(QFileDialog.getSaveFileName(self, "Export plugin", "plugins/%s_plugin.py"%name, "*.py"))
        #plugin_name = os.path.basename(plugin_filename).replace(".py","")
        script = tab.get_script().replace("\n", "\n        ")
        for func in self.controller.func_manager.functions():
            script = script.replace("%s(" % func.class_name, "self.%s(" % func.class_name)
        script = script.replace("model", "self.model")
        script = script.replace("gui", "self.gui")

        if os.path.isdir('plugins'):
            f = open('./plugins/%s.py' % plugin_name, 'w')
        else:
            f = open('../plugins/%s.py' % plugin_name, 'w')
        f.write("""
from appfuncs.AppFunc import AppFunc
class %s(AppFunc):

    def __init__(self, controller, gui, model):
        AppFunc.__init__(self, controller, gui, model, "%s",main_menu_pos=%s,popup_menu_pos=%s)

    def run(self, *args, **kwargs):
        %s""" % (plugin_name, plugin_text, menu_pos, menu_pos, script))
        f.close()
        app_func = self.controller.func_manager.add_func("plugins.%s" % plugin_name, plugin_name, True)
        self.controller.func_manager.add_to_menu(app_func)

    def load_script(self):
        self._load_script(self.filename)

    def _load_script(self, filename):
        try:
            f = open(filename)
            script = f.read()
            f.close()
            return script
        except:
            return ""

    def set_output(self, output):
        self.ui.textEditOutput.setText(output)

    def set_position(self, line):
        self.ui.labelLineNumber.setText("Line: %d" % line)

    def get_obj(self, name):
        try:
            return eval(name)
        except:
            return None



class Seq_Script(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)

@singleton
class ScriptingDialogWindow(ScriptingWindow, QtDialogLoader):
    def __init__(self, controller, gui, model):
        module = ScriptingWindowUI
        try: self.ui = module.Ui_Form()
        except: pass
        QtDialogLoader.__init__(self, module, gui, modal=False)
        self.setParent(None)
        ScriptingWindow.__init__(self, controller, gui, model)

        self.setModal(False)
        print (self.modal)

    def closeEvent(self, *args, **kwargs):
        self.close()
        return QtDialogLoader.closeEvent(self, *args, **kwargs)


class ScriptingMainWindow(QtMainWindowLoader, ScriptingWindow, QtUI):

    def __init__(self, controller, model):
        module = ScriptingWindowUI
        try: self.ui = module.Ui_Form()
        except: pass

        QtMainWindowLoader.__init__(self, module, self)
        ScriptingWindow.__init__(self, controller, self, model)
        QtUI.__init__(self, self)

    def closeEvent(self, *args, **kwargs):
        self.close()
        return QtMainWindowLoader.closeEvent(self, *args, **kwargs)






