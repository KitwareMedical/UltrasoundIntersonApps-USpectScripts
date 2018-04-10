#!/usr/bin/python

import os
import imp
import fnmatch
import argparse

def ApplyPyToFolder(script, folder, glob='*.nrrd', script_args=None):
    print("Folder = " + folder)
    print("Script = " + script)
    print("Extra Arg = ", script_args)

    script_file_dir, script_file_name_ext = os.path.split(script)
    script_module_name, script_file_ext = os.path.splitext(script_file_name_ext)
    script_module = imp.load_source(script_module_name, script)
    script_class = getattr(script_module, script_module_name)

    file_list = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, glob):
            file_list.append(os.path.join(root, filename))
    number_of_files = len(file_list)
    print("Number of files = " + str(number_of_files))
    for i, input_file in enumerate(file_list):
        print("%d of %d: %s" %(i, number_of_files, input_file))
        script_class(input_file, *script_args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply processing script to files in a folder.')
    parser.add_argument('script', help='Path to script to run. Should have a function with the same as the script to invoke')
    parser.add_argument('folder', help='Folder to apply the script to.')
    parser.add_argument('--glob', help='Glob to find files recursively in the given folder.', default='*.nrrd')
    parser.add_argument('extra_script_args', nargs='*', help='extra arguments to pass to script function')
    args = parser.parse_args()
    ApplyPyToFolder(args.script, args.folder, args.glob, args.extra_script_args)
