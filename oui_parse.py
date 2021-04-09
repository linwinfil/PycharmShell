import os
import sys

root = "D:/gomo/python/PycharmShell/ieee/"
src_file_path = root + "oui.txt"

dst_file_name = "nmap-mac-prefixes"
dst_file_path = root + dst_file_name

if os.path.exists(src_file_path):
    with open(src_file_path) as fos:
        line = fos.readline()
        while line:
            print(line)
            line = fos.readline()

# if os.path.exists(dst_file_path):
#     os.remove(dst_file_path)
# with open(dst_file_path, 'w') as fos:
#     fos.write("x")
