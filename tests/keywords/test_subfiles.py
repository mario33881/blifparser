import os
import sys
import unittest

# import fsm.py from the ../../blifparser/keywords folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
keywords_fsm_path = os.path.join(curr_dir, "..", "..", "blifparser", "keywords")
sys.path.insert(1, os.path.realpath(keywords_fsm_path))
import subfiles  # noqa: E402


class TestSubfiles(unittest.TestCase):

    def test_search(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_params = ["", "  "]
        correct_params = [
            {"param": "124 ", "repr": "Search('124')", "str": ".search 124"},
            {"param": "   234  ", "repr": "Search('234')", "str": ".search 234"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                search = subfiles.Search(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain something
        for param in valueerrors_params:
            with self.assertRaises(ValueError, msg="'{}' should contain the wrong amount "
                                                   "of parameters or non numeric params".format(param)) as e:
                search = subfiles.Search(param)

            self.assertEqual(e.exception.args[0], ".search needs one parameter")

        # correct parameter: object should contain data and its representation should be correct
        for funcparam in correct_params:
            search = subfiles.Search(funcparam["param"])
            self.assertEqual(search.filepath, funcparam["param"].strip())
            self.assertEqual(search.__repr__(), funcparam["repr"])
            self.assertEqual(search.__str__(), funcparam["str"])

    def test_subckt(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "00", "ab", "  a   ", "a   ", "   1"]
        valueerrors_wrong_second_param = ["a b", "a -", "a o", "a None", "a False"]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                subckt = subfiles.Subckt(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain two parameters only
        for param in valueerrors_num_params:
            with self.assertRaises(ValueError, msg="'{}' should contain the wrong amount of parameters".format(param)) as e:
                subckt = subfiles.Subckt(param)

            self.assertEqual(e.exception.args[0], ".subckt expects at least two parameters")

        # should throw ValueErrors: the second parameter should contain an equal sign
        for param in valueerrors_wrong_second_param:
            with self.assertRaises(ValueError, msg="'{}' should fail because the second parameter "
                                                   "doesn't contain an equal sign".format(param)) as e:
                subckt = subfiles.Subckt(param)

            self.assertIn("parameter is incorrect (there needs to be an equal sign '=')", e.exception.args[0])

        # correct parameters: object should contain data and its representation should be correct
        subckt = subfiles.Subckt(" circuit a=b  ")
        self.assertEqual(subckt.modelname, "circuit")
        self.assertIn("a=b", subckt.params)
        self.assertEqual(subckt.__repr__(), "Subckt('circuit a=b')")
        self.assertEqual(subckt.__str__(), ".subckt circuit a=b")


if __name__ == "__main__":
    unittest.main()
