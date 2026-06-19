import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

def find_files_containing(query, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if query.lower() in file.lower():
                print(os.path.join(root, file))

find_files_containing("swatch", "f:/BAO_SAPO/sapo_new")
