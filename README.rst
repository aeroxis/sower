Sower
=====

How to Install
--------------

.. code:: bash

    $ pip install sower

Why Do You Need Sower?
**********************


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
YAML like the following file:

.. code:: 

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

Let's call this as `sower-contract.yml`. Now we simply tell Sower where to create these
files, and the path to this contract.

If we want to create files based on this contract on `/home/davydany/foobar`, we would do 
the following:

.. code:: bash

    $ sower /home/davydany/foobar /tmp/sower-contract.yml

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
    from sower.farm import sow

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
            sow(self.contract, self.root)
