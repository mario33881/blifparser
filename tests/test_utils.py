import os
import sys
import unittest

# import fsm.py from the ../../blifparser/keywords folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
blifparser_path = os.path.join(curr_dir, "..", "blifparser")
sys.path.insert(1, os.path.realpath(blifparser_path))
import utils  # noqa: F401, E402


class TestUtils(unittest.TestCase):
    @unittest.skip("TODO: write add_metadata() tests")
    def test_add_metadata(self):
        pass

    @unittest.skip("TODO: write remove_comments() tests")
    def test_remove_comments(self):
        pass

    @unittest.skip("TODO: write remove_params_newline() tests")
    def test_remove_params_newline(self):
        pass


if __name__ == "__main__":
    unittest.main()
