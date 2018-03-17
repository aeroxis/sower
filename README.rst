[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Faeroxis%2Fsower.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Faeroxis%2Fsower?ref=badge_shield)

.. image:: https://raw.githubusercontent.com/aeroxis/sower/master/img/sower-logo.png
    :alt: Sultan logo
    :align: right
    :width: 300px
    :scale: 50%

.. image:: https://badge.fury.io/py/sower.png
    :target: https://badge.fury.io/py/sower

.. image:: https://travis-ci.org/aeroxis/sower.svg?branch=master
    :target: https://travis-ci.org/aeroxis/sower

.. image:: http://img.shields.io/:license-mit-blue.svg
  :alt: MIT License
  :target: http://doge.mit-license.org

Sower
=====

**Sower "plants" directories, files and symlinks on your filesystem based on a contract you tell it.**


How to Install
--------------

.. code:: bash

    $ pip install sower

Why Do You Need Sower?
======================


The Problem
-----------

Have you ever been in a situation where you needed to create a large set of 
files, that may span multiple subdirectories? You might need to do this for
testing, especially if your application that you're testing is supposed to 
be tested for how it manages a set of files based on their directory 
structure.

The Solution - Part 1
---------------------

Sower is the solution for this problem! You simply define a *contract* in
YAML or JSON like the following:

+---------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| YAML (sower-contract.yml)                                                             + JSON (sower-contract.json)                                                                    +
+=======================================================================================+===============================================================================================+
|                                                                                       |                                                                                               |
| .. code::                                                                             | .. code::                                                                                     |
|                                                                                       |                                                                                               |
|     ---                                                                               |     {                                                                                         |
|     sower:                                                                            |         "sower": {                                                                            |
|         plan:                                                                         |             "plan": {                                                                         |
|             bin:                                                                      |                 "bin": {                                                                      |
|                 start.sh:                                                             |                     "start.sh": {                                                             |
|                     type: file                                                        |                         "type": "file",                                                       |
|                     content: "echo 'Starting foobar'"                                 |                         "content": "echo'Startingfoobar'"                                     |
|                 stop.sh:                                                              |                     },                                                                        |
|                     type: file                                                        |                     "stop.sh": {                                                              |
|                     content: "echo 'Stopping foobar'"                                 |                         "type": "file",                                                       |
|             data:                                                                     |                         "content": "echo'Stoppingfoobar'"                                     |
|                 test-data.tar.gz:                                                     |                     }                                                                         |
|                     type: file                                                        |                 },                                                                            |
|                     content: "!random!"                                               |                 "data": {                                                                     |
|                     size: 1Mb                                                         |                     "test-data.tar.gz": {                                                     |
|             src:                                                                      |                         "type": "file",                                                       |
|                 foobar:                                                               |                         "content": "!random!",                                                |
|                     __init__.py:                                                      |                         "size": "1Mb"                                                         |
|                         type: file                                                    |                     }                                                                         |
|                         content: "# just a comment"                                   |                 },                                                                            |
|                     main.py:                                                          |                 "src": {                                                                      |
|                         type: file                                                    |                     "foobar": {                                                               |
|                         content: >                                                    |                         "__init__.py": {                                                      |
|                             import os\n                                               |                             "type": "file",                                                   |
|                             print('Foo Bar: %s' % os.path.abspath('.'))\n\n           |                             "content": "#justacomment"                                        |
|                     link_main.py:                                                     |                         },                                                                    |
|                         type: symlink                                                 |                         "main.py": {                                                          |
|                         target: ../foobar/main.py                                     |                             "type": "file",                                                   |
|                                                                                       |                             "content": "importos\nprint('FooBar: %s'%os.path.abspath('.')\n\n |
|                                                                                       |                         },                                                                    |
|                                                                                       |                         "link_main.py": {                                                     |
|                                                                                       |                             "type": "symlink",                                                |
|                                                                                       |                             "target": "../foobar/main.py"                                     |
|                                                                                       |                         }                                                                     |
|                                                                                       |                     }                                                                         |
|                                                                                       |                 }                                                                             |
|                                                                                       |             }                                                                                 |
|                                                                                       |         }                                                                                     |
|                                                                                       |     }                                                                                         |
+---------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+

Save the Contract to disk (choose either YAML or JSON listing from above). Now 
we simply tell Sower where to create these files, and the path to this contract.

If we want to create files based on this contract on `/home/davydany/foobar`, we would do 
the following:

If you chose the YAML, run the following:
.. code:: bash

    $ sower sow /home/davydany/foobar /tmp/sower-contract.yml

If you chose the JSON, run the following:
.. code:: bash

    $ sower sow /home/davydany/foobar /tmp/sower-contract.json

This would create the following structure:

.. code:: bash

    /home/davydany/foobar
    ├── bin
    │   ├── start.sh
    │   └── stop.sh
    ├── data
    │   └── test-data.tar.gz
    └── src
        └── foobar
            ├── __init__.py
            ├── link_main.py -> /tmp/foobar/src/foobar/main.py
            └── main.py

    4 directories, 6 files


The Solution - Part 2
---------------------

Now, suppose you need to do this in your integration tests that use python's `unittest`. You
can still leverage this with the Sower API.

You would have something like this in your test's `setUp` method.

.. code::

    import tempfile
    import unittest
    from sower.sow import perform_sow

    class TestMyApp(unittest.TestCase):

        def setUp(self):

            self.root = tempfile.mkdtemp('_farmer_test')
            self.contract = """

            ---
            sower:
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
            perform_sow(self.root, self.contract)


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Faeroxis%2Fsower.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Faeroxis%2Fsower?ref=badge_large)