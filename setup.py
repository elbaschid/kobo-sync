import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

requires = ['requests', 'peewee', 'click']
tests_require = ['pytest', 'pytest-cache', 'pytest-cov']


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="kobo-sync",
    version='0.0.0',
    description="Sync Kobo bookmarks",
    long_description="\n\n".join([open("README.rst").read()]),
    license='MIT',
    author="Sebastian Vetter",
    author_email="seb@roadsi.de",
    url="https://kobo-sync.readthedocs.org",
    packages=['kobo_sync'],
    install_requires=requires,
    entry_points={'console_scripts': [
        'kobo_sync = kobo_sync.cli:main']},
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython'],
    extras_require={'test': tests_require},
    cmdclass={'test': PyTest})
