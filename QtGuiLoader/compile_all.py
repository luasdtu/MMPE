'''
Created on 18/06/2012

@author: Mads
'''
from MyQt import ui_compiler
import os
import sys



def _compile_all(path, compiler):

    def get_ui_list(path):
        ui_list = []
        if os.path.isdir(path):
            #search files and sub-packages
            for f in os.listdir(path):
                if f not in ['dist']:
                    ui_list += get_ui_list(os.path.join(path, f))
        else:
            #search file
            if path.endswith(".ui"):
                ui_list.append(path)
        return ui_list

    exe_dir = os.path.dirname(sys.executable)
    os.environ['path'] = "%s;%s;%s/scripts" % (os.environ['path'], exe_dir, exe_dir)
    os.environ['WINPYDIR'] = exe_dir
    for ui_file in get_ui_list(path):
        py_file = ui_file.replace(".ui", ".py")


        if os.path.exists(py_file):
            with open(py_file) as fid:
                if compiler == "pyuic4":
                    recompile = "PySide" in fid.read()
                else:
                    recompile = "PyQt4" in fid.read()
        #recompile = 1
        if not os.path.exists(py_file) or \
            os.path.getmtime(ui_file) > os.path.getmtime(py_file) or \
            os.path.getsize(py_file) == 0 or \
            recompile:
            print ("compile %s > %s" % (ui_file, py_file))



            os.system("%s %s > %s" % (compiler, ui_file, py_file))

        else:
            #print "%s: ok" % py_file
            pass
    print ("Finish compiling UI")


def compile_all(path="."):
    print ("ui_compiler" + ui_compiler)
    _compile_all(path, ui_compiler)

def compile_all_pyqt(path="."):
    os.environ['QT_API'] = "pyqt"
    _compile_all(path, "pyuic4")

def compile_all_pyside(path="."):
    os.environ['QT_API'] = "pyside"
    _compile_all(path, "pyside-uic")

if "__main__" == __name__:
    import os
    path = r"C:\mmpe\python\pydap_redmine\trunk"
    print (os.path.realpath(path))
    compile_all_pyside(path)
