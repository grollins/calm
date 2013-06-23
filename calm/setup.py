import os
# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration('calm', parent_package, top_path)
    config.add_subpackage('test')
    config.add_data_dir('test_data')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup as np_setup
    np_setup(**configuration(top_path='').todict())
