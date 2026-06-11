import os

def list_all_files():
    for root, dirs, files in os.walk('sapo_BWT_new'):
        for file in files:
            print(os.path.join(root, file))

list_all_files()
