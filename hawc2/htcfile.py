'''
Created on 20/01/2014

@author: MMPE
'''

from __future__ import division, absolute_import, unicode_literals
from collections import OrderedDict
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np


class HTCFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        with open(filename) as fid:
            for l in fid.readlines():
                if ";" in l and len(l.strip()) != 1:
                    self.lines.append(l.lower()[:l.index(";")].replace("\t", " ").strip())

        self.sections = self.parse_section()




    def parse_section(self, startline=0):
        global curr_line
        section = OrderedDict()
        curr_line = startline
        while curr_line < len(self.lines):
            line = self.lines[curr_line]
            if line.startswith("begin "):
                key = line[6:]
                curr_line += 1
                value = self.parse_section(curr_line)
                if key in section:
                    if not isinstance(section[key], list):
                        section[key] = [section[key], value]
                    else:
                        section[key].append(value)
                else:
                    section[key] = value
            elif line.startswith("end "):
                return section
            elif " " in line:
                d = line.index(" ")
                key = line[:d]

                value = line[d:].strip()
                if key in section:
                    if not isinstance(section[key], list):
                        section[key] = [section[key], value]
                    else:
                        section[key].append(value)
                else:
                    section[key] = value
            curr_line += 1
        return section


    def save(self, filename):
        with open(filename, 'w') as fid:
            fid.write(self.section2str(self.sections))

    def section2str(self, section, level=0):
        s = ""
        for k, vs in section.items():
            for v in ([vs], vs)[isinstance(vs, list)]:
                if isinstance(v, OrderedDict):
                    s += "%sbegin %s;\n" % ("  "*level, k)
                    s += self.section2str(v, level + 1)
                    s += "%send %s;\n;\n" % ("  "*level, k)
                else:
                    s += "%s%s %s;\n" % ("  "*(level), k, v)
        return s


if "__main__" == __name__:
    f = HTCFile(r"C:\mmpe\programming\Fortran\DTU10MWRef\htc\dtu_10mw_rwt.htc")
    print (f.section2str(f.sections['new_htc_structure']['main_body'][0]))



