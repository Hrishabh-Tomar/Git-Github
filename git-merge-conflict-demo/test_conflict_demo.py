import shutil
import unittest

import conflict_demo


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class ConflictDemoTests(unittest.TestCase):
    def test_conflict_is_created_and_resolved(self):
        conflict_demo.run(verbose=False)


if __name__ == "__main__":
    unittest.main()
