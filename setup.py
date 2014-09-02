import os
from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build
from distutils.dir_util import copy_tree, remove_tree
from setuptools.command.develop import develop

def get_submodules_and_fix_paths():
    if path.exists('.git'):
        # Get HEAD version
        check_call(['rm', '-rf', 'epiceditor/static/epiceditor'])
        check_call(['git', 'reset', '--hard'])
        # Get submodules
        check_call(['git', 'submodule', 'init'])
        check_call(['git', 'submodule', 'update'])
        # Reset EpicEditor to tag 0.2.0
        check_call(['cd', 'epiceditor/static/epiceditor', '&&', 'git', 'reset', '--hard', '0.2.2'], shell=True)
        # Move contents of epiceditor and remove .git
        dst = "epiceditor/static/epiceditor/"
        src = "epiceditor/static/epiceditor/epiceditor/"
        copy_tree(src, dst)
        remove_tree(src)

class build_with_submodules(build):
    def run(self):
        get_submodules_and_fix_paths()
        build.run(self)

class develop_with_submodules(develop):
    def run(self):
        get_submodules_and_fix_paths()
        develop.run(self)


setup(
  name = "django-epiceditor",
  version = "0.2.3",
  author = "Remi Barraquand",
  author_email = "dev@remibarraquand.com",
  url = "https://github.com/barraq/django-epiceditor",
  description = ("A django app that allows the easy addition of EpicEditor markdown editor to a django form field, whether in a custom app or the Django Admin."),
  long_description = open('README.rst').read(),
  packages = ['epiceditor'],
  include_package_data = True,
  install_requires = [
    "Django >= 1.3",
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    ],
  license='LICENSE',
  cmdclass={"build": build_with_submodules, "develop": develop_with_submodules},
)
