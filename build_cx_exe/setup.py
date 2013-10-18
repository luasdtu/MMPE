from cx_Freeze import setup, Executable


build_exe_options = {
"includes": [],
"packages": [],
'excludes' : ['PyQt4.uic.port_v3', 'Tkconstants','tcl', 'tk', 'doctest','pdb', 'MSVCP90.dll'],
"include_files": []}

setup(
name = "pydap",
version="0.15.15",
description="",
author = "",
options = { "build_exe": build_exe_options},
executables = [Executable("pydap.py", shortcutName="pydap", shortcutDir="DesktopFolder")])
    