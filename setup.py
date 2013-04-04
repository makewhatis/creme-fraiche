import os
import sys

import sys
from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

py_version = sys.version_info[:2]

PY3 = py_version[0] == 3

if PY3:
    if py_version < (3, 2):
        raise RuntimeError('On Python 3, Space requires Python 3.2 or better')
else:
    if py_version < (2, 6):
        raise RuntimeError('On Python 2, Space requires Python 2.6 or better')

version = "0.0.2"

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_beaker',
    'whoosh',
    'psycopg2',
]

tests_require = [
    'mock >= 1.0.1',
    'pytest',
    'pytest-cov',
    'coverage',
    'virtualenv',  # for scaffolding tests
    'WebTest >= 1.3.1',  # py3 compat
]

if not PY3:
    tests_require.append('unittest2>=0.5.1')


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['creme_fraiche/tests', '--capture=sys']
        self.test_suite = True

    def run_tests(self):
         #import here, cause outside the eggs aren&#039;t loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='creme_fraiche',
      version='0.0',
      description='creme_fraiche',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='creme_fraiche',
      install_requires=requires,
      tests_require=tests_require,
      cmdclass={'test': PyTest},
      entry_points="""\
      [paste.app_factory]
      main = creme_fraiche:main
      [console_scripts]
      initialize_creme_fraiche_db = creme_fraiche.scripts.initializedb:main
      """,
      )
