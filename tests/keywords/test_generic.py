import os
import sys
import unittest

# import fsm.py from the ../../blifparser/keywords folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
keywords_fsm_path = os.path.join(curr_dir, "..", "..", "blifparser", "keywords")
sys.path.insert(1, os.path.realpath(keywords_fsm_path))
import generic  # noqa: E402, F401


class TestGeneric(unittest.TestCase):
    
    def test_model(self):
        """
        Tests the Model() class which represents the .model keyword in BLIF files.
        """
        with self.assertRaises(TypeError):
            generic.Model(None)
        
        with self.assertRaises(ValueError):
            generic.Model("")
        
        with self.assertRaises(ValueError):
            generic.Model(" ")
        
        with self.assertRaises(ValueError):
            generic.Model("too many parameters")
        
        model = generic.Model(" valid_name ")
        self.assertEqual(model.name, "valid_name")

    def test_inputs(self):
        """
        Tests the Inputs() class which represents the .inputs keyword in BLIF files.
        """
        with self.assertRaises(TypeError):
            generic.Inputs(None)
        
        with self.assertRaises(ValueError):
            generic.Inputs("")
        
        with self.assertRaises(ValueError):
            generic.Inputs(" ")
        
        inputs = generic.Inputs(" valid number of parameters ")
        self.assertEqual(inputs.inputs, ["valid", "number", "of", "parameters"])

    def test_outputs(self):
        """
        Tests the Outputs() class which represents the .outputs keyword in BLIF files.
        """
        with self.assertRaises(TypeError):
            generic.Outputs(None)
        
        with self.assertRaises(ValueError):
            generic.Outputs("")
        
        with self.assertRaises(ValueError):
            generic.Outputs(" ")
        
        outputs = generic.Outputs(" valid number of parameters ")
        self.assertEqual(outputs.outputs, ["valid", "number", "of", "parameters"])

    def test_names(self):
        """
        Tests the Names() class which represents the .names keyword in BLIF files.

        TODO: test truth tables
        """
        with self.assertRaises(TypeError):
            generic.Names(None, False)
        
        with self.assertRaises(TypeError):
            generic.Names("", None)
        
        with self.assertRaises(ValueError):
            generic.Names("", False)
        
        with self.assertRaises(ValueError):
            generic.Names(" ", False)
        
        # one parameter: 0 inputs, 1 output
        names1 = generic.Names(" constant ", False)
        self.assertEqual(names1.inputs, [])
        self.assertEqual(names1.output, "constant")
        self.assertFalse(names1.is_dontcare)

        # multiple parameters: x inputs, 1 output
        names2 = generic.Names(" valid number of parameters ", False)
        self.assertEqual(names2.inputs, ["valid", "number", "of"])
        self.assertEqual(names2.output, "parameters")
        self.assertFalse(names2.is_dontcare)

    def test_latch(self):
        """
        Tests the Latch() class which represents the .latch keyword in BLIF files.
        """
        with self.assertRaises(TypeError):
            generic.Latch(None)
        
        # not enough parameters
        with self.assertRaises(Exception):
            generic.Latch(" ")
        
        with self.assertRaises(Exception):
            generic.Latch(" a ")
        
        # too many parameters
        with self.assertRaises(Exception):
            generic.Latch(" too many parameters for this component ")
        
        # wrong type
        with self.assertRaises(ValueError):
            generic.Latch(" input output wrong_type control initval ")
        
        # wrong initval
        with self.assertRaises(ValueError):
            generic.Latch(" input output re control wrong_initval ")

        latch1 = generic.Latch(" input output re control 0 ")
        self.assertEqual(latch1.input, "input")
        self.assertEqual(latch1.output, "output")
        self.assertEqual(latch1.type, "re")
        self.assertEqual(latch1.control, "control")
        self.assertEqual(latch1.initval, "0")

    @unittest.skip("TODO: write Blif() tests")
    def test_blif(self):
        pass


if __name__ == "__main__":
    unittest.main()
