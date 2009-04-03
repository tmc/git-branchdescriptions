#!/usr/bin/env python
"""
git-branchdescriptions

Author: Travis Cline <travis.cline@gmail.com>
License: Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
import os
import sys
import optparse
import re
import git
from git.errors import GitCommandError

__version__ = (0, 0, 2)

class BranchDescriptions(object):

    def __init__(self, repo_path=None, options=None, args=None):
        if not repo_path:
            repo_path = os.getcwd()
        self.repo = git.Repo(repo_path)
        self.options = options
        self.args = args

    def set(self, name, value=None):
        if not name:
            try:
                name = self.repo.active_branch
            except GitCommandError:
                print 'Error: apparently not on an active branch.'
                return False

        self.repo.git.execute(('git',
                               'config',
                               'branchdescriptions.%s' %
                                   _santitize_branch_name(name),
                               value,
                               ))
        return True

    def get(self, name):
        return self.repo.git.execute(('git',
                                      'config',
                                      '--get',
                                      'branchdescriptions.%s' %
                                          _santitize_branch_name(name)),
                                      with_exceptions=False)

    def show(self, *args):
        command = ['git', 'branch']
        if not self.options.no_color:
            command.append('--color')
        if self.options.verbosity:
            command.append('-v')
        if self.options.remotes:
            command.append('-r')
        if self.options.all:
            command.append('-a')
        branches = self.repo.git.execute(command).split('\n')

        for branch in branches:
            if branch:
                name = _santitize_branch_name(branch)
                desc = self.get(name)
                if desc:
                    branch = '%s - %s' % (branch, desc)
                print branch
        return True

    def run(self):
        if self.options.set:
            return self.set(self.options.branch, ' '.join(self.args))
        else:
            return self.show()

def _santitize_branch_name(name):
    """
    Strips down a git branch name to plain text.
    """
    s = name.strip('*').strip().split()[0] # get first part of string sans '*'
    s = _strip_ansi_escaped_chars(s) # remove color formatting if it exists
    rep = '---'
    for to_rep in ['/', '_']:
        s = s.replace(to_rep, rep)
    return s

def _strip_ansi_escaped_chars(s):
    """
    Strips ANSI escaped characters from a string.
    """
    esc = '\x1b.+?m'
    return re.sub(esc+'$', '', re.sub('^'+esc, '', s))

def execute_from_command_line(argv=None):
    usage = """usage: %prog [options]
Use --set to set the branch's description.
Example: git branchdescriptions --set This branch addresses issue foo."""
    op = optparse.OptionParser(usage=usage, version=__version__, option_list=(
        optparse.Option('-v', '--verbosity', action="store_true",
            help='Show sha1 and commit subject lines'),
        optparse.Option('-r', '--remotes', action="store_true",
            help='List remote branches'),
        optparse.Option('-a', '--all', action="store_true",
            help='List both local and remote branches'),
        optparse.Option('-s', '--set', action="store_true",
            help="Use to set the branch's description"),
        optparse.Option('-b', '--branch',
            help='Which branch to operate on. Optional, assumes current branch'),
        optparse.Option('--no-color', action="store_true",
            help='Skip color formatting (for dumb terminals)'),
    ))

    options, args = op.parse_args()

    if args and not options.set:
        op.error('use --set to set branch description')

    app = BranchDescriptions(options=options, args=args)
    retval = app.run()
    sys.exit(retval == False)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
