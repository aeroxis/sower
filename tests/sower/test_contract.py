import unittest

from sower.contract import Contract


class ContractTestCase(unittest.TestCase):

    def setUp(self):

        self.contract = """
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

        handle, self.contract_path = tempfile.mkstemp(
            suffix='.yml', 
            prefix='contract',
            dir=None,
            text=True)

        handle.write(self.contract)
        handle.close()

    def test_contract_load(self):

        contract = Contract(self.contract_path)
        
        self.assertIsNotNone(contract.plan)
        self.assertIsNotNone(contract.config)
