try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import exifsort

setup(
        name='exifsort',
        version=exifsort.__version__,
        author='Byron D. Peebles',
        author_email='byron.peebles@gmail.com',
        scripts=['exifsort.py'],
        license='LICENSE.txt',
        description='Sort files from a single directory to dated ones based on exif data.',
        long_description=open('README.rst').read(),
)
