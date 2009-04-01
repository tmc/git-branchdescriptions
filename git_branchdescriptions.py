#!/usr/bin/env python
import os
import sys
import re
import optparse
import git

__version__ = (0, 0, 1)

class BranchDescriptions(object):

    def __init__(self, repo_path=None, options=None, args=None):
        if not repo_path:
            repo_path = os.getcwd()
        self.repo = git.Repo(repo_path)
        self.options = options
        self.args = args

    def set(self, name, value=None):
        if not value:
            value = name
            name = self.repo.active_branch
        self.repo.git.execute(('git',
                               'config',
                               'branchdescriptions.%s' % name,
                               value,
                               ))
        return True

    def get(self, name):
        return self.repo.git.execute(('git config --get branchdescriptions.%s' % name).split(), with_exceptions=False)

    def show(self, *args):
        command = ['git', 'branch']
        if self.options.verbosity:
            command.append('-v')
        if self.options.remotes:
            command.append('-r')
        if self.options.all:
            command.append('-a')
        branches = self.repo.git.execute(command).split('\n')

        for branch in branches:
            if branch:
                name = branch.strip('*').strip().split()[0]
                desc = self.get(name)
                if desc:
                    branch = '%s - %s' % (branch, desc)
                print branch


    def run(self):
        if self.options.set:
            return self.set(' '.join(self.args))
        else:
            return self.show()


if __name__ == '__main__':

    op = optparse.OptionParser(version=__version__, option_list=(
        optparse.Option('-v', '--verbosity', action="store_true"),
        optparse.Option('-r', '--remotes', action="store_true"),
        optparse.Option('-a', '--all', action="store_true"),
        optparse.Option('-s', '--set', action="store_true"),
    ))

    options, args = op.parse_args()

    if args and not options.set:
        op.error('use --set to set branch description')

    app = BranchDescriptions(options=options, args=args)
    sys.exit(app.run())
