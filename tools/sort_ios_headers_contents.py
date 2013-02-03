#!/usr/bin/python

"""
Overwrites the headers with their contents-sorted version.
The goal is to ease comparision between versions.

$ cd iOS-Runtime-Headers
$ python sort_ios_headers_contents.py 
"""

import os

def write_header_description(filepath, first_lines, ivars, properties, class_methods, instance_methods):

    with open (filepath, 'w') as f:

        for l in first_lines:
            f.write(l)
        for l in ivars:
            f.write(l)
        f.write("}\n\n")
        
        for l in properties:
            f.write(l)
        if len(properties):
            f.write("\n")
        
        for l in class_methods:
            f.write(l)
        if len(class_methods):
            f.write("\n")
        
        for l in instance_methods:
            f.write(l)
        if len(instance_methods):
            f.write("\n")

        f.write("@end\n")

def sort_header(path_in, path_out):

    ivars = []
    properties = []
    class_methods = []
    instance_methods = []
    
    first_lines = []
    has_seen_interface = False
    
    with open(path_in, 'r') as f:
        for line in f:
            
            if not has_seen_interface:
                if line.startswith("/* Generated by RuntimeBrowser"):
                    # remove version to ease diff comparision
                    line = "/* Generated by RuntimeBrowser\n"

                # remove extraneous new lines
                if len(first_lines) > 0 and len(first_lines[-1]) is 1 and len(line) is 1:
                    continue
                
                if line.startswith('@interface'):
                    has_seen_interface = True
                    if not line.endswith('{\n'):
                        line = line[:-1] + ' {\n'
                    if line.endswith('  {\n'):
                        line = line[:-4] + ' {\n'
                
                first_lines.append(line)
                continue
            
            if line is '{\n':
                first_lines = first_lines[:-1]
    
            if line.startswith('    '):
                ivars.append(line)
            elif line.startswith('@property'):
                properties.append(line)
            elif line.startswith('+'):
                class_methods.append(line)
            elif line.startswith('-'):
                instance_methods.append(line)
    
    ivars = sorted(ivars, key = lambda s: s.replace('*', '').split(' ')[-1])
    properties = sorted(properties, key = lambda s: s.split(' ')[-1])
    class_methods = sorted(class_methods, key = lambda s: ')'.join(s.split(')')[1:]))
    instance_methods = sorted(instance_methods, key = lambda s: ')'.join(s.split(')')[1:]))

    write_header_description(path_out, first_lines, ivars, properties, class_methods, instance_methods)

for root, dirs, files in os.walk('.'):
    
    headers = (f for f in files if f.endswith(".h"))
    
    for f in headers:
        path = os.path.join(root, f)
        print path
        
        sort_header(path, path)
        