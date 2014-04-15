'''
Created on 17/03/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals
from ui.scripting_window.controller import ScriptingWindowController
import os
from functions.process_exec import pexec
import sys
from functions import process_exec
from ui.scripting_window import script_function
import re
from functions import argument_string
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np


import shutil
import os


def copy_doc(doc_path):
    #shutil.rmtree(dst_path, ignore_errors=True)
    shutil.copytree(os.path.join(doc_path, 'templates/_static'), os.path.join(doc_path, '_static/'))

    shutil.copy2(os.path.join(doc_path, 'sphinx/_build/html/ScriptFunctions.html'), doc_path)
    shutil.copytree(os.path.join(doc_path, 'sphinx/_build/html/_modules'), os.path.join(doc_path, '_modules'))
    template = os.path.join(doc_path, "templates/template.html")
    shutil.copy2(template, os.path.join(doc_path, "doc.html"))
    shutil.copy2(template, os.path.join(doc_path, "source.html"))
    shutil.copy2(template, os.path.join(doc_path, "index.html"))


def make_doc(doc_path, appfunc_path):
    for folder in ['_modules', '_static', '_sources']:
        shutil.rmtree(os.path.join(doc_path, folder), ignore_errors=True)

    appfunc_lst = script_function.script_function_class_list(appfunc_path)

    with open('docs/ui.scripting_window.rst', 'w') as fid:
        header = "Scripting_window Package"
        fid.write('%s\n%s\n\n' % (header, "="*len(header)))
        for module in set([appfunc.__module__ for appfunc in appfunc_lst]):
            s = ':mod:`%s` Module' % module.split(".")[-1]  #somefunctions
            fid.write('%s\n%s\n\n' % (s, "-"*len(s)))
            fid.write('.. automodule:: %s\n' % module)  #ui.scripting_window.appfuncs.somefunctions
            fid.write("""    :members:
    :undoc-members:
    :show-inheritance:\n\n""")
#

    sphinx_path = os.path.join(doc_path, "sphinx")
    errorcode, stdout, stderr = pexec(["make.bat", "html"], sphinx_path)
    print (stdout)
    sys.stderr.write(stderr)
    sys.stderr.flush()

    if errorcode == 0:
        copy_doc(doc_path)

        lst = script_function.script_function_class_list(appfunc_path)

        for appfunc in lst:

            module = appfunc.__module__
            name = appfunc.__name__
            arguments = argument_string(appfunc.run)

        abc_lst = sorted(set([appfunc.__name__[0].upper() for appfunc in lst]))
        index_html = '<h1 id="index">Index</h1>'
        index_html += '<div class="genindex-jumpbox">\n'
        index_html += "\n|".join(['<a href="#%s"><strong>%s</strong></a>' % (abc, abc) for abc in abc_lst])
        index_html += '\n</div>\n\n'
        for abc in abc_lst:
            index_html += '<h2 id="%s">%s</h2>\n' % (abc, abc)
            index_html += '<table style="width: 100%" class="indextable genindextable"><tr>\n'
            for appfunc in [appfunc for appfunc in lst if appfunc.__name__[0].upper() == abc]:
                module = appfunc.__module__.replace(appfunc_path.replace("/", ".") + ".", "")
                name = appfunc.__name__
                arguments = argument_string(appfunc.run)
                index_html += '\n<tr><td style="width: 33%" valign="top"><dl>'

                index_html += '<dt><a href="doc.html#%s"><tt class="descclassname">%s.</tt><tt class="descname"><big>%s</big>' % (appfunc, module, name)
                index_html += arguments.replace("(", '<big>(</big><em>').replace(',', '</em>, <em>').replace(')', '</em><big>)</big>')
                index_html += '</tt></a></dt></dl></td>'
                index_html += '</tr>'

            index_html += '</table>'

        with open(os.path.join(doc_path, 'index.html'), 'r') as fid:
            html = fid.read()
        with open(os.path.join(doc_path, 'index.html'), 'w') as fid:
            fid.write(html.replace("#Contents", index_html))

#        pattern = 'class="descclassname">[^<]+<'  #</tt><tt class="descname">MyFirstFunction</tt><big>(</big>'
#        print re.findall(pattern, docs)
        #print re.findall('<tt class="descclassname">ui.scripting_window.appfuncs.somefunctions.</tt><tt class="descname">MyFirstFunction</tt><big>(</big>', docs)


if __name__ == "__main__":
    make_doc("ui/scripting_window/docs", 'ui/scripting_window/appfuncs')
    controller = ScriptingWindowController()
