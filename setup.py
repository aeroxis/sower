from setuptools import setup, find_packages

with open("./README.rst") as f:
    LONG_DESCRIPTION = f.read()

with open("./VERSION") as f:
    VERSION = f.read().strip()

print("Found Packages: ", find_packages('src'))

setup(
    name='sower',
    description='Sower "plants" directories, files and symlinks on your filesystem based on a contract you tell it.',
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    author='David Daniel',
    author_email='davydany@aeroxis.com',
    license='MIT',
    packages=find_packages('src', exclude=('tests', )),
    package_dir={'': 'src'},
    install_requires=[
        'PyYAML>=3.12',
        'click>=6.7',
        'simplejson>=3.10.0'
    ],
    url='http://github.com/aeroxis/sower',
      entry_points="""
            [console_scripts]
                sower = sower.sow:sower
      """,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Unix Shell",
        "License :: OSI Approved :: MIT License"]
)
