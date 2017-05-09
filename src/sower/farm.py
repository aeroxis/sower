import click
import grp
import logging
import math
import os
import pwd
import re
import textwrap
import yaml

from sultan.api import Sultan

from sower.utils import Loader

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger('farmer')


FILE_SIZE_REGEX = "(?P<numeric>[\d]+){1}(?P<si_unit>(k|M|G|T|P|E|Z|Y)){0,1}b"
FILE_SIZE_REGEX_PATTERN = re.compile(FILE_SIZE_REGEX)

def file_size_in_bytes(size):
    """
    Given a valid 'size' that matches the FILE_SIZE_REGEX,
    this method returns the size in bytes.
    """
    matched = FILE_SIZE_REGEX_PATTERN.match(size)
    if matched:

        # determine how big of a file we need
        numeric_value = matched.group('numeric')
        si_unit = matched.group('si_unit')
        si_units = [None, 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
        power = si_units.index(si_unit)

        size_in_bytes = int(int(numeric_value) * math.pow(1024, power))
        return size_in_bytes
    else:
        return 0


def mkdir(path):

    if not os.path.exists(path):
        os.makedirs(path)

def mkfile(path, contents, user, group, size):

    if contents == "!random!":
        # convert size to bytes
        size_in_bytes = file_size_in_bytes(size)
        with open(path, 'wb') as filehandle:
            content = '\0'
            filehandle.seek(size_in_bytes-1)
            filehandle.write(content.encode('utf-8'))
    else:
        # create file with contents
        with open(path, 'w') as filehandle:
            filehandle.write(contents)

    # set permissions
    uid = pwd.getpwnam(user).pw_uid if user else os.stat(path).st_uid
    gid = grp.getgrnam(group).gr_gid if group else os.stat(path).st_gid
    os.chown(path, uid, gid)
    if not os.path.exists(path):
        raise IOError("Unable to create '%s'" % path)


def mksymlink(target_path, link_path):
    """
    Makes a symbolic link
    """
    if not os.path.exists(target_path):
        raise IOError("'%s' does not exist. The Target Path needs to exist first." % target_path)

    if os.path.exists(link_path):
        raise IOError("'%s' already exists. The Link Path must not exist." % link_path)

    os.symlink(target_path, link_path)

def sow(root, contract):
    """
    Makes a forest of directories, files, symlinks and any other file-like objects
    on the given directory 'root', based on what is specified in the contract.
    """
    
    for item, contents in contract.items():

        path_to_item = os.path.join(root, item)
        item_type = contents.get('type', 'dir')

        if item_type is 'dir':

            mkdir(path_to_item)
            sow(path_to_item, contents)

        elif item_type == 'file':

            file_contents = contents.get('content')
            user = contents.get('user')
            group = contents.get('group')
            size = contents.get('size')

            mkfile(path_to_item, file_contents, user, group, size)

        elif item_type in ('symlink', 'link'):

            target = contents.get('target')
            if target.startswith('../'):
                target = os.path.abspath(os.path.join(root, target))

            mksymlink(target, path_to_item)

@click.group()
def sower():

    pass

@sower.command()
@click.argument('root', type=click.Path(exists=False))
@click.argument('path_to_contract', type=click.Path(exists=True))
def farm(root, path_to_contract):
    """
    Creates a set of files based on the files specified in this farm
    """

    # load the contract
    contract = None
    with open(path_to_contract) as contract_file:
        contract = contract_file.read()

    # make the forest
    if contract:

        loaded_contract = yaml.load(
            textwrap.dedent(contract),
            Loader=Loader)
        
        # get root element 'farmer'
        sower_instructions = loaded_contract.get('sower', {})
        if not sower_instructions:
            click.secho('You need to have a root level key called "farmer".', fg='red')
            return -1

        # get the plan
        plan = sower_instructions.get('plan')
        if not plan:
            click.secho('You need to have a 2nd level key called "plan" under "farmer" with the resources you would like to create.', fg='red')
            return -1

        if loaded_contract:
            sow(root, plan)
            
        else:
            click.secho('The Contract File is Empty.', fg='red')
