from unittest import TestCase
from tempfile import gettempdir
import git
from random import randint

randstring = lambda x=5: ''.join([chr(randint(ord('a'), ord('z'))) for y in range(x)])

from git_branchdescriptions import BranchDescriptions

class TestBranchDescriptions(TestCase):
    
    def setUp(self):
        self.git_dir = gettempdir()
        self.repo = git.Repo()
        self.repo.create(self.git_dir)

    def test_basic_setting_and_retrieval(self):
        bd = BranchDescriptions(self.git_dir)
        desc = randstring()
        bd.set('foobar', desc)
        self.assertEqual(desc, bd.get('foobar'))

    def test_setting_persistence(self):
        bd = BranchDescriptions(self.git_dir)
        desc = randstring()
        bd.set('foobar', desc)

        bd = BranchDescriptions(self.git_dir)
        self.assertEqual(desc, bd.get('foobar'))
