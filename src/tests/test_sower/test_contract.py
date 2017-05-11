import os
import tempfile
import unittest

from sower.contract import Contract

class ContractTestCase(unittest.TestCase):

    def setUp(self):

        self.yaml_contract = YAML_CONTRACT
        self.json_contract = JSON_CONTRACT

        handle, self.yaml_contract_path = tempfile.mkstemp(
            suffix='.yml', 
            prefix='yaml_contract',
            dir=None,
            text=True)

        with open(self.yaml_contract_path, 'w') as f:
            f.write(self.yaml_contract)

        handle, self.json_contract_path = tempfile.mkstemp(
            suffix='.json',
            prefix='json_contract',
            dir=None,
            text=True)

        with open(self.json_contract_path, 'w') as f:
            f.write(self.json_contract)

    def tearDown(self):

        os.remove(self.yaml_contract_path)
        os.remove(self.json_contract_path)

    def test_yaml_contract_load(self):

        contract = Contract(self.yaml_contract_path)
        
        self.assertIsNotNone(contract.plan)
        self.assertIsNotNone(contract.config)

    def test_json_contract_load(self):

        contract = Contract(self.json_contract_path)

        self.assertIsNotNone(contract.plan)
        self.assertIsNotNone(contract.config)

    def test_equality(self):

        yaml_contract = Contract(self.yaml_contract_path)
        json_contract = Contract(self.json_contract_path)


class YAMLContractTestCase(unittest.TestCase):

    def setUp(self):


        self.yaml_contract = YAML_CONTRACT

        handle, self.yaml_contract_path = tempfile.mkstemp(
            suffix='.yml', 
            prefix='yaml_contract',
            dir=None,
            text=True)

        with open(self.yaml_contract_path, 'w') as f:
            f.write(self.yaml_contract)

    def tearDown(self):

        os.remove(self.yaml_contract_path)

    def test_valid_values(self):

        contract = Contract(self.yaml_contract_path)

        self.assertIsNotNone(contract.config)
        self.assertIsNotNone(contract.plan)

        self.assertEqual(contract.config.get('param1'), 'foobar')
        self.assertEqual(contract.config.get('param2'), 'barbaz')

        self.assertIn('start.sh', contract.plan['bin'])
        self.assertIn('stop.sh', contract.plan['bin'])
        self.assertIn('test-data.tar.gz', contract.plan['data'])


class JSONContractTestCase(unittest.TestCase):

    def setUp(self):


        self.json_contract = JSON_CONTRACT

        handle, self.json_contract_path = tempfile.mkstemp(
            suffix='.json', 
            prefix='json_contract',
            dir=None,
            text=True)

        with open(self.json_contract_path, 'w') as f:
            f.write(self.json_contract)

    def tearDown(self):

        os.remove(self.json_contract_path)

    def test_valid_values(self):

        contract = Contract(self.json_contract_path)

        self.assertIsNotNone(contract.config)
        self.assertIsNotNone(contract.plan)

        self.assertEqual(contract.config.get('param1'), 'foobar')
        self.assertEqual(contract.config.get('param2'), 'barbaz')

        self.assertIn('start.sh', contract.plan['bin'])
        self.assertIn('stop.sh', contract.plan['bin'])
        self.assertIn('test-data.tar.gz', contract.plan['data'])

YAML_CONTRACT = """
---
sower:
    config:
        param1: 'foobar'
        param2: 'barbaz'
    plan:
        bin:
            start.sh:
                type: file
                content: "echo 'Starting foobar'"
            stop.sh:
                type: file
                content: "echo 'Stopping foobar'"
        data:
            test-data.tar.gz:
                type: file
                content: "!random!"
                size: 1Mb
        src:
            foobar:
                __init__.py:
                    type: file
                    content: "# just a comment"
                main.py:
                    type: file
                    content: >
                        import os\n
                        print('Foo Bar: %s' % os.path.abspath('.'))\n\n
                link_main.py:
                    type: symlink
                    target: ../foobar/main.py
"""

JSON_CONTRACT = """
{
  "sower": {
    "config": {
      "param1": "foobar",
      "param2": "barbaz"
    },
    "plan": {
      "bin": {
        "start.sh": {
          "type": "file",
          "content": "echo 'Starting foobar'"
        },
        "stop.sh": {
          "type": "file",
          "content": "echo 'Stopping foobar'"
        }
      },
      "data": {
        "test-data.tar.gz": {
          "type": "file",
          "content": "!random!",
          "size": "1Mb"
        }
      },
      "src": {
        "foobar": {
          "__init__.py": {
            "type": "file",
            "content": "# just a comment"
          },
          "main.py": {
            "type": "file",
            "content": "import os\\n print('Foo Bar: %s' % os.path.abspath('.'))\\n\\n\\n"
          },
          "link_main.py": {
            "type": "symlink",
            "target": "../foobar/main.py"
          }
        }
      }
    }
  }
}
"""