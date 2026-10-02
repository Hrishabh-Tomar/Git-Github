import shutil
import unittest

import stash_workflow_demo


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class StashWorkflowTests(unittest.TestCase):
    def test_full_stash_workflow(self):
        stash_workflow_demo.run(verbose=False)


if __name__ == "__main__":
    unittest.main()
