import os
import simplejson as json
import textwrap
import yaml

from collections import OrderedDict

def create_random_file(path, size_kb):
    """
    Creates a file with at 'path', with size 'size_kb' 
    """
    
    chunks = int(size_kb /(1024*10))
    if chunks == 0:
        chunks = 1
    with open(path,"wb") as fh:
        for iter in range(chunks):
            numrand = os.urandom(int(size_kb*1024 / chunks))
            fh.write(numrand)        
        numrand = os.urandom(int(size_kb*1024 % chunks))
        fh.write(numrand)
