from __future__ import division, print_function, absolute_import, \
    unicode_literals
import cython_compile
import sys
import textui
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass

sys.path.append(".")

def size_from_file(selfilename):
    with open(selfilename) as f:
        info = f.readlines()[8].split()
        scans = int(info[0])
        no_sensors = int(info[1])
    return (scans, no_sensors)






def ascii2bin(ascii_selfilename, bin_selfilename=None, ui=textui.TextUI()):

    # Convert dat file
    ascii_datfilename = ascii_selfilename.replace(".sel", '.dat')
    if bin_selfilename is None:
        bin_selfilename = ascii_selfilename[:-4] + "_bin.sel"
    ui.show_message("Converting %s \nto\n %s" % (ascii_selfilename, bin_selfilename))
    cython_compile.cython_import('hawc2ascii2bin.cy_dat_ascii2bin')
    from hawc2ascii2bin.cy_dat_ascii2bin import dat_ascii2bin_progress

    size = size_from_file(ascii_selfilename)

    scale_factors = dat_ascii2bin_progress(ascii_datfilename, bin_selfilename.replace('.sel', '.dat'), size, ui=ui)

    # Read, convert and write sel file
    with open(ascii_selfilename) as f:
        lines = f.readlines()

    #lines[1] = "  Version ID : Pydap %d.%d\n" % (version.__version__[:2])
    lines[5] = "  Result file : %s.dat\n" % bin_selfilename[:-4]
    lines[8] = lines[8].replace("ASCII", 'BINARY')

    lines.append("Scale factors:\n")
    for sf in scale_factors:
        lines.append("  %.5E\n" % sf)
    with open(bin_selfilename, 'w') as f:
        f.writelines(lines)
    if ui is not None:
        ui.show_message("Finish converting %s to %s" % (ascii_selfilename, bin_selfilename))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("syntax: ascii2bin ascii_sel_filename [bin_sel_filename]")
    elif len(sys.argv) == 2:
        ascii2bin(sys.argv[1])
    else:
        ascii2bin(sys.argv[1], sys.argv[2])
