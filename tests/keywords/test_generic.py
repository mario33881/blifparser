import os
import sys
import unittest

# import fsm.py from the ../../blifparser/keywords folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
keywords_fsm_path = os.path.join(curr_dir, "..", "..", "blifparser", "keywords")
sys.path.insert(1, os.path.realpath(keywords_fsm_path))
import generic  # noqa: E402, F401


class TestGeneric(unittest.TestCase):
    @unittest.skip("TODO: write Model() tests")
    def test_model(self):
        pass

    @unittest.skip("TODO: write Inputs() tests")
    def test_inputs(self):
        pass

    @unittest.skip("TODO: write Outputs() tests")
    def test_outputs(self):
        pass

    @unittest.skip("TODO: write Names() tests")
    def test_names(self):
        pass

    @unittest.skip("TODO: write Latch() tests")
    def test_latch(self):
        pass

    @unittest.skip("TODO: write Blif() tests")
    def test_blif(self):
        pass


if __name__ == "__main__":
    unittest.main()
