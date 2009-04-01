#!/usr/bin/env python
from setuptools import setup, find_packages
from git_branchdescriptions import __version__

setup(name='git-branchdescriptions',
    version='%s.%s.%s' % __version__,
    description='git-branchdescriptions',
    long_description=open('README').read(),
    author='Travis Cline',
    author_email='travis.cline@gmail.com',
    url='http://github.com/traviscline/git-branchdescriptions/',
    license='MIT',
    packages=find_packages(),
    install_requires = ['GitPython'],
    platforms = ["any"],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'git-branchdescriptions = git_branchdescriptions:execute_from_command_line',
        ],
    },
    py_modules=['git_branchdescriptions'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
    ],
)
