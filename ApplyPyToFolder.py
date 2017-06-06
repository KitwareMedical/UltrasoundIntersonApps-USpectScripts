#!/usr/bin/python

import sys
import os
import imp
import glob

def ApplyPyToFolder(script, folder, script_arg=""):
    print("Folder = " + folder)
    print("Script = " + script)
    print("Extra Arg = " + script_arg)

    script_file_dir, script_file_name_ext = os.path.split(script)
    script_module_name, script_file_ext = os.path.splitext(script_file_name_ext)
    script_module = imp.load_source(script_module_name, script)
    script_class = getattr(script_module, script_module_name)

    file_list = glob.glob(os.path.join(folder, '*.nrrd'))
    number_of_files = len(file_list)
    print("Number of files = " + str(number_of_files))
    for i, input_file in enumerate(file_list):
        print("%d of %d: %s" %(i, number_of_files, input_file))
        if len(script_arg) == 0:
            script_class(input_file)
        else:
            script_class(input_file, script_arg)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        script = sys.argv[1]
        folder = sys.argv[2]
        ApplyPyToFolder(script, folder)
    elif len(sys.argv) == 4:
        script = sys.argv[1]
        folder = sys.argv[2]
        script_arg = sys.argv[3]
        ApplyPyToFolder(script, folder, script_arg)
    else:
        print("ApplyPyToFolder <script> <folder> [extra_script_arg]")
