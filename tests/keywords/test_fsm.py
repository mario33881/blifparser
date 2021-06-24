import os
import sys
import unittest

# import fsm.py from the ../../blifparser/keywords folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
keywords_fsm_path = os.path.join(curr_dir, "..", "..", "blifparser", "keywords")
sys.path.insert(1, os.path.realpath(keywords_fsm_path))
import fsm  # noqa: E402


class TestFSM(unittest.TestCase):

    def test_fsm(self):
        testfsm = fsm.Fsm()

        # Nothing set
        with self.assertRaises(ValueError, msg="should throw a ValueError because .i is not set") as e:
            testfsm.is_valid()
        self.assertEqual(e.exception.args[0], ".i must be set")
        self.assertEqual(len(testfsm.get_state_names()), 0, "there shouldn't be states in an empty table")

        # Set .i
        i = fsm.I("2")
        testfsm.i = i

        # Only .i is set
        with self.assertRaises(ValueError, msg="should throw a ValueError because .o is not set") as e:
            testfsm.is_valid()
        self.assertEqual(e.exception.args[0], ".o must be set")
        self.assertEqual(len(testfsm.get_state_names()), 0, "there shouldn't be states in an empty table")

        # Set .o
        o = fsm.O("2")
        testfsm.o = o

        # Only .i and .o are set: minimal configuration
        self.assertTrue(testfsm.is_valid(), "Should be the minimal accepted configuration")
        self.assertEqual(len(testfsm.get_state_names()), 0, "there shouldn't be states in an empty table")

        # Add incorrect transition table
        testfsm.transtable.append([])

        # Validation should fail: each row needs to have 4 elements
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because the transition table row doesn't have all the info needed"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(
            e.exception.args[0],
            "'' row of the transition table doesn't have all the expected data (<input> <current-state> <next-state> <output>)"
        )
        self.assertEqual(len(testfsm.get_state_names()), 0, "there shouldn't be states in an empty table")

        # "Fix" first row of the transition table
        testfsm.transtable[0] = ["a", "b", "c", "d"]

        # Validation should fail: the first element needs to be made out of ones and zeros (and don't cares)
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because the first element of the row "
                "needs to be made out of ones and zeros (and don't cares)"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(e.exception.args[0], "'a' input of the 'a b c d' row (transition table) "
                                              "has unexpected characters (accepted chars are ['0', '1', '-'])")
        states = testfsm.get_state_names()
        self.assertEqual(len(states), 2, "there should be two states ('b' and 'c')")
        self.assertIn("b", states, "'b' should be a state")
        self.assertIn("c", states, "'c' should be a state")

        # "Fix" first row: putting ones and zeros in the first element
        testfsm.transtable[0] = ["1", "test", "second", "d"]

        # Validation should fail: the first element needs to have two elements (i.num is 2)
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because the first element needs to have two elements (i.num is 2)"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(e.exception.args[0], "'1 test second d' row (transition table) has an unexpected number "
                                              "of inputs (found 1 elements in '1' but expected 2 based on the .i parameter)")
        states = testfsm.get_state_names()
        self.assertEqual(len(states), 2, "there should be two states ('test' and 'second')")
        self.assertIn("test", states, "'test' should be a state")
        self.assertIn("second", states, "'second' should be a state")

        # "Fix" first row: the first element has the correct amount of elements
        testfsm.transtable[0] = ["10", "another", "test", "d"]

        # Validation should fail: the last element needs to be made out of ones and zeros (and don't cares)
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because the last element of "
                "the row needs to be made out of ones and zeros (and don't cares)"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(
            e.exception.args[0],
            "'d' output of the '10 another test d' row (transition table) "
            "has unexpected characters (accepted chars are ['0', '1', '-'])"
        )

        states = testfsm.get_state_names()
        self.assertEqual(len(states), 2, "there should be two states ('another' and 'test')")
        self.assertIn("test", states, "'test' should be a state")
        self.assertIn("another", states, "'another' should be a state")

        # "Fix" first row: the last element is made of accepted chars
        testfsm.transtable[0] = ["10", "another", "test", "10-"]

        # Validation should fail: the last element needs to have 2 output
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because the last element of the row needs to have 2 outputs"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(
            e.exception.args[0],
            "'10 another test 10-' row (transition table) has an unexpected number "
            "of outputs (found 3 elements in '10-' but expected 2 based on the .o parameter)"
        )

        states = testfsm.get_state_names()
        self.assertEqual(len(states), 2, "there should be two states ('another' and 'test')")
        self.assertIn("test", states, "'test' should be a state")
        self.assertIn("another", states, "'another' should be a state")

        # Fix first row
        testfsm.transtable[0] = ["10", "another", "test", "-1"]

        self.assertTrue(testfsm.is_valid(), "Should be ok")

        states = testfsm.get_state_names()
        self.assertEqual(len(states), 2, "there should be two states ('another' and 'test')")
        self.assertIn("test", states, "'test' should be a state")
        self.assertIn("another", states, "'another' should be a state")

        # Set .p
        p = fsm.P("2")
        testfsm.p = p

        # Validation should fail: there's only one row in the transition table
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because there's only one row in the transition table"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(
            e.exception.args[0],
            ".p <num-terms> has incorrect <num-terms> value "
            "(it should be '1' instead of '2' because the transition table has that amount of rows)"
        )

        # Set .p correctly
        testfsm.p.num = "1"
        self.assertTrue(testfsm.is_valid(), "Should be ok")

        # Set .s
        s = fsm.S("4")
        testfsm.s = s

        # Validation should fail: there are only two states in the transition table
        with self.assertRaises(ValueError, msg="should throw a ValueError because "
                                               "there are only two states in the transition table") as e:
            testfsm.is_valid()
        self.assertEqual(e.exception.args[0], ".s <num-states> has incorrect <num-states> value "
                                              "(it should be '2' instead of '4' because the transition "
                                              "table contains that amount of unique states)")

        # Set .s correctly
        testfsm.s.num = "2"
        self.assertTrue(testfsm.is_valid(), "Should be ok")

        # Set .r
        r = fsm.R("nonexistingstate")
        testfsm.r = r

        # Validation should fail: 'nonexistingstate' is not present in the transition table
        with self.assertRaises(
            ValueError,
            msg="should throw a ValueError because 'nonexistingstate' is not present in the transition table"
        ) as e:
            testfsm.is_valid()

        self.assertEqual(e.exception.args[0], ".r <reset-state> has incorrect <reset-state> value "
                                              "(can't find 'nonexistingstate' in the transition table)")

        # Set .r correctly
        testfsm.r.name = "test"
        self.assertTrue(testfsm.is_valid(), "Should be ok")

    def test_i(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "0  0", "a   b   ", "a b c", "a   b   c", "   1a ab"]
        correct_params = [
            {"param": "124 ", "repr": "I('124')", "str": ".i 124"},
            {"param": "   234  ", "repr": "I('234')", "str": ".i 234"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                i = fsm.I(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain one numeric parameter only
        for param in valueerrors_num_params:
            with self.assertRaises(
                ValueError,
                msg="'{}' should contain the wrong amount of parameters or non numeric params".format(param)
            ) as e:
                i = fsm.I(param)

            self.assertEqual(e.exception.args[0], ".i parameter needs to be numeric (it must be made of digits 0-9)")

        # correct parameter: object should contain data and its representation should be correct
        for funcparam in correct_params:
            i = fsm.I(funcparam["param"])
            self.assertEqual(i.num, funcparam["param"].strip())
            self.assertEqual(i.__repr__(), funcparam["repr"])
            self.assertEqual(i.__str__(), funcparam["str"])

    def test_o(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "0  0", "a   b   ", "a b c", "a   b   c", "   1a ab"]
        correct_params = [
            {"param": "124 ", "repr": "O('124')", "str": ".o 124"},
            {"param": "   234  ", "repr": "O('234')", "str": ".o 234"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                o = fsm.O(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain one numeric parameter only
        for param in valueerrors_num_params:
            with self.assertRaises(
                ValueError,
                msg="'{}' should contain the wrong amount of parameters or non numeric params".format(param)
            ) as e:
                o = fsm.O(param)

            self.assertEqual(e.exception.args[0], ".o parameter needs to be numeric (it must be made of digits 0-9)")

        # correct parameter: object should contain data and its representation should be correct
        for funcparam in correct_params:
            o = fsm.O(funcparam["param"])
            self.assertEqual(o.num, funcparam["param"].strip())
            self.assertEqual(o.__repr__(), funcparam["repr"])
            self.assertEqual(o.__str__(), funcparam["str"])

    def test_s(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "0  0", "a   b   ", "a b c", "a   b   c", "   1a ab"]
        correct_params = [
            {"param": "124 ", "repr": "S('124')", "str": ".s 124"},
            {"param": "   234  ", "repr": "S('234')", "str": ".s 234"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                s = fsm.S(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain one numeric parameter only
        for param in valueerrors_num_params:
            with self.assertRaises(
                ValueError,
                msg="'{}' should contain the wrong amount of parameters or non numeric params".format(param)
            ) as e:
                s = fsm.S(param)

            self.assertEqual(e.exception.args[0], ".s parameter needs to be numeric (it must be made of digits 0-9)")

        # correct parameter: object should contain data and its representation should be correct
        for funcparam in correct_params:
            s = fsm.S(funcparam["param"])
            self.assertEqual(s.num, funcparam["param"].strip())
            self.assertEqual(s.__repr__(), funcparam["repr"])
            self.assertEqual(s.__str__(), funcparam["str"])

    def test_p(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "0  0", "a   b   ", "a b c", "a   b   c", "   1a ab"]
        correct_params = [
            {"param": "124 ", "repr": "P('124')", "str": ".p 124"},
            {"param": "   234  ", "repr": "P('234')", "str": ".p 234"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                p = fsm.P(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain one numeric parameter only
        for param in valueerrors_num_params:

            with self.assertRaises(
                ValueError,
                msg="'{}' should contain the wrong amount of parameters or non numeric params".format(param)
            ) as e:

                p = fsm.P(param)

            self.assertEqual(e.exception.args[0], ".p parameter needs to be numeric (it must be made of digits 0-9)")

        # correct parameter: object should contain data and its representation should be correct
        for funcparam in correct_params:
            p = fsm.P(funcparam["param"])
            self.assertEqual(p.num, funcparam["param"].strip())
            self.assertEqual(p.__repr__(), funcparam["repr"])
            self.assertEqual(p.__str__(), funcparam["str"])

    def test_r(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "0  0", "a   b   ", "a b c", "a   b   c", "   1a ab"]
        correct_params = [
            {"param": "a0a ", "repr": "R('a0a')", "str": ".r a0a"},
            {"param": "   test  ", "repr": "R('test')", "str": ".r test"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                r = fsm.R(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain one parameter only
        for param in valueerrors_num_params:
            with self.assertRaises(ValueError, msg="'{}' should contain the wrong amount of parameters".format(param)) as e:
                r = fsm.R(param)

            self.assertEqual(
                e.exception.args[0],
                ".r accepts (and needs) only one parameter (the parameter can't contain spaces)"
            )

        # correct parameter: object should contain data and its representation should be correct
        for funcparam in correct_params:
            r = fsm.R(funcparam["param"])
            self.assertEqual(r.name, funcparam["param"].strip())
            self.assertEqual(r.__repr__(), funcparam["repr"])
            self.assertEqual(r.__str__(), funcparam["str"])

    def test_code(self):
        typeerrors_params = [1, None, {}, [], ()]
        valueerrors_num_params = ["", "  ", "00", "ab", "a b c", "a   b   c", "   1"]
        valueerrors_wrong_second_param = ["a b", "a -", "a o", "a None", "a False"]
        correct_params = [
            {"param": "a 0", "repr": "Code('a 0')", "str": ".code a 0"},
            {"param": "test   01010  ", "repr": "Code('test 01010')", "str": ".code test 01010"},
            ]

        # should throw TypeErrors
        for param in typeerrors_params:
            with self.assertRaises(TypeError, msg="'{}' shouldn't be a valid parameter type".format(param)) as e:
                code = fsm.Code(param)

            self.assertEqual(e.exception.args[0], "'{}' is not a string".format(param))

        # should throw ValueErrors: string must contain two parameters only
        for param in valueerrors_num_params:
            with self.assertRaises(ValueError, msg="'{}' should contain the wrong amount of parameters".format(param)) as e:
                code = fsm.Code(param)

            self.assertEqual(e.exception.args[0], ".code expects two parameters")

        # should throw ValueErrors: the second parameter should contain ones and/or zeros
        for param in valueerrors_wrong_second_param:
            with self.assertRaises(ValueError, msg="'{}' should contain bad second parameter".format(param)) as e:
                code = fsm.Code(param)

            string_params = [el for el in param.split(" ") if el != ""]
            state_name = string_params[0]
            state_encoding = string_params[1]
            self.assertEqual(
                len(string_params),
                2,
                "Something is wrong in the tests dataset called 'valueerrors_wrong_second_param' ({})".format(param)
            )

            error_msg = "Unexpected char in the state encoding " \
                        "(only '0's and '1's are accepted): .code " + state_name + " " + state_encoding

            self.assertEqual(e.exception.args[0], error_msg)

        # correct parameters: object should contain data and its representation should be correct
        for funcparam in correct_params:
            string_params = [el for el in funcparam["param"].split(" ") if el != ""]
            state_name = string_params[0]
            state_encoding = string_params[1]

            self.assertEqual(
                len(string_params),
                2,
                "Something is wrong in the tests dataset called 'correct_params[\"param\"]' ({})".format(funcparam)
            )

            code = fsm.Code(funcparam["param"])
            self.assertEqual(code.state_name, state_name)
            self.assertEqual(code.state_encoding, state_encoding)
            self.assertEqual(code.__repr__(), funcparam["repr"])
            self.assertEqual(code.__str__(), funcparam["str"])


if __name__ == "__main__":
    unittest.main()
