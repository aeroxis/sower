import os
import simplejson as json
import textwrap
import yaml

from collections import OrderedDict

from sower.utils.yaml_loader import Loader as YAMLLoader


class Contract(object):

    def __init__(self, path):

        self.path = path
        self.contract = load_contract_from_file(path)

    @property
    def plan(self):
        """
        Returns the 'plan' portion of the contract.
        """
        return self.contract.get('sower', {}).get('plan')

    @property
    def config(self):
        """
        Returns the 'config' portion of the contract. 

        NOTE: The 'config' portion is OPTIONAL, so 
        this method might return None.
        """
        return self.contract.get('sower', {}).get('config')

def load_contract_from_file(path):

    # load contract from the file system into memory
    contract_contents = None
    with open(path, 'r') as f:
        contract_contents = f.read()

    # find the appropriate loader based on file ending
    contract = None
    if path.endswith('.yml') or path.endswith('.yaml'):
        contract = load_yaml_data(contract_contents)
    elif path.endswith('.json'):
        contract = load_json_data(contract_contents)
    else:
        raise ValueError('Invalid Data Format. Your File must end in'\
            ' .json, .yml or .yaml')

    # validate the contract
    validate_contract(contract)
    return contract
    
def load_yaml_data(contract_contents):
    """
    Given a string 'contract_contents', this method assumes it's 
    contents are YAML, and loads it into memory.
    """
    return yaml.load(
        textwrap.dedent(contract_contents),
        Loader=YAMLLoader
    )

def load_json_data(contract_contents):
    """
    Given a string 'contract_contents', this method assumes it's
    contents are JSON, and loads it into memory
    """
    return json.loads(
        contract_contents, object_pairs_hook=OrderedDict
    )

        
def validate_contract(contract):
    """
    Validates the given contract. Contract must be of type 'dict'.
    """
    if len(contract) != 1:
        raise ValueError('Root Level of Contract must contain '\
            '1 element: sower')

    if 'sower' not in contract:
        raise ValueError('"sower" is not the root level element '\
            'in the contract.')

    plan = contract.get('sower', {}).get('plan')
    if not plan:
        raise ValueError("A plan was not specified in the contract."\
            " The 2nd level must contain a 'plan' element.")
    