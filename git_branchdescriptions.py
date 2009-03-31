#!/usr/bin/env python
import os
import sys
import git

class BranchDescriptions(object):

    def __init__(self, repo_path=None):
        if not repo_path:
            repo_path = os.getcwd()
        self.repo = git.Repo(repo_path)

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
        branches = self.repo.git.execute(['git', 'branch', '-v']).split('\n')
        for branch in branches:
            name = branch.strip('*').strip().split()[0]
            desc = self.get(name)
            if desc:
                branch = '%s - %s' % (branch, desc)
            print branch

def usage():
    return """%s cmd""" % __file__

if __name__ == '__main__':

    handlers = {
        1: 'show',
        2: 'set',
    }

    handler = handlers.get(len(sys.argv), None)

    if not handler:
        print 'No handler for this number of arguments.'
        print usage()
        sys.exit(1)

    app = BranchDescriptions()
    f = getattr(app, handler, None)

    if not callable(f):
        print usage()
        sys.exit(1)
    else:
        sys.exit(f(*sys.argv[1:]))
