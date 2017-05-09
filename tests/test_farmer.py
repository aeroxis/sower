import math
import os
import shutil
import tempfile
import unittest
import yaml

from farmer.farm import (file_size_in_bytes, mkdir, mkfile, mksymlink, make_forest)
from farmer.utils import Loader


class TestFileSizeInBytes(unittest.TestCase):

    def calculate_power(self, power):

        return int(250) * math.pow(1024, power)

    def test_file_size_in_bytes(self):

        self.assertEqual(
            file_size_in_bytes('250b'), 250)

        self.assertEqual(
            file_size_in_bytes('250kb'), self.calculate_power(1))

        self.assertEqual(
            file_size_in_bytes('250Mb'), self.calculate_power(2))

        self.assertEqual(
            file_size_in_bytes('250Gb'), self.calculate_power(3))

        self.assertEqual(
            file_size_in_bytes('250Tb'), self.calculate_power(4))

        self.assertEqual(
            file_size_in_bytes('250Pb'), self.calculate_power(5))

        self.assertEqual(
            file_size_in_bytes('250Eb'), self.calculate_power(6))

        self.assertEqual(
            file_size_in_bytes('250Zb'), self.calculate_power(7))

        self.assertEqual(
            file_size_in_bytes('250Yb'), self.calculate_power(8))

class TestMakeDir(unittest.TestCase):

    def setUp(self):

        self.test_dir = '/tmp/test-directory'

    def tearDown(self):
        
        shutil.rmtree(self.test_dir)
        self.assertFalse(os.path.exists(self.test_dir))

    def test_mkdir(self):

        self.assertFalse(os.path.exists(self.test_dir))
        mkdir(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))


class TestMakeFile(unittest.TestCase):

    def setUp(self):

        self.test_file = '/tmp/test-file'

    def tearDown(self):

        os.remove(self.test_file)

    def test_make_simple_file(self):

        mkfile(self.test_file, '', None, None, None)

        self.assertTrue(os.path.exists(self.test_file))

    def test_make_file_of_certain_size(self):

        mkfile(self.test_file, '!random!', None, None, '250Mb')

        self.assertTrue(os.path.exists(self.test_file))
        self.assertEqual(os.path.getsize(self.test_file), 250 * 1024 * 1024)

class TestMakeSymlink(unittest.TestCase):

    def setUp(self):

        self.source_file = '/tmp/test-source-file'
        self.link_file = '/tmp/link-file'

    def tearDown(self):

        os.remove(self.source_file)
        os.remove(self.link_file)

    def test_make_link(self):

        self.assertFalse(os.path.exists(self.source_file))
        self.assertFalse(os.path.exists(self.link_file))

        mkfile(self.source_file, '!random!', None, None, '250b')
        mksymlink(self.source_file, self.link_file)

        self.assertTrue(os.path.exists(self.source_file))
        self.assertTrue(os.path.exists(self.link_file))

class TestMakeForest(unittest.TestCase):

    def setUp(self):

        self.test_dir = tempfile.mkdtemp('_farmer_test')
        self.contract = yaml.load("""
---
farmer:
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

        """, Loader=Loader)['farmer']

    def tearDown(self):
        
        # if os.path.exists(self.test_dir):
        #     shutil.rmtree(self.test_dir)
        pass

    def path_to(self, path):

        return os.path.join(self.test_dir, path)

    def assert_path_exists(self, path):

        abs_path = self.path_to(path)
        exists = os.path.exists(abs_path)
        self.assertTrue(exists, "'%s' does not exist." % abs_path)

    def assert_has_content(self, path, actual_content):

        with open(self.path_to(path)) as f:

            content = f.readlines()
            for actual_line in actual_content:
                self.assertIn(actual_line, content)

    def assert_valid_symlink(self, target, link):

        self.assertTrue(os.path.exists(self.path_to(target)), "'%s' does not exist." % self.path_to(target))
        self.assertTrue(os.path.exists(self.path_to(link)), "'%s' does not exist." % self.path_to(link))

        self.assertEqual(
            self.path_to(target),
            os.readlink(self.path_to(link)))

    def test_make_forest(self):

        make_forest(self.contract, self.test_dir)

        # assert that the directories are created properly
        self.assert_path_exists('bin')
        self.assert_path_exists('bin/start.sh')
        self.assert_path_exists('bin/stop.sh')
        self.assert_path_exists('data')
        self.assert_path_exists('data/test-data.tar.gz')
        self.assert_path_exists('src')
        self.assert_path_exists('src/foobar')
        self.assert_path_exists('src/foobar/__init__.py')
        self.assert_path_exists('src/foobar/main.py')

        # assert that the files are created properly
        self.assert_has_content('bin/start.sh', ["echo 'Starting foobar'"])
        self.assert_has_content('bin/stop.sh', ["echo 'Stopping foobar'"])
        self.assert_has_content('src/foobar/__init__.py', ["# just a comment"])
        self.assert_has_content('src/foobar/main.py',
            ["import os\n", "print('Foo Bar: %s' % os.path.abspath('.'))\n"])

        # assert that the symlinks are valid
        print("test_dir: ", self.test_dir)
        self.assert_valid_symlink('src/foobar/main.py', 'src/foobar/link_main.py')