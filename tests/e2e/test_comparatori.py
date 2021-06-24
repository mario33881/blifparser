import os
import sys
import unittest
import urllib.request as urllib
import tempfile

try:
    import httplib
except ImportError:
    import http.client as httplib

# import fsm.py from the ../../blifparser/keywords folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
blifparser_path = os.path.join(curr_dir, "..", "..", "blifparser")
sys.path.insert(1, os.path.realpath(blifparser_path))
import blifparser  # noqa: E402

baseurl = "https://raw.githubusercontent.com/arc6-202021/lib_componenti_sis/1041cc3fb4998fa1a509b3381a136ad626330cb4/"


def have_internet():
    """
    Returns True if the Internet connection is present.
    """
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


class TestComparatori(unittest.TestCase):

    def test_comparatore2(self):
        fileurl = baseurl + "comparatori/comparatore2.blif"

        # request the file
        blif_file = urllib.urlopen(fileurl)

        # create a temporary folder to download the file
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'tmp_file')

            # write the BLIF file to a local file
            with open(f_name, 'wb') as fh:
                line = blif_file.readline()
                while line.decode() != "":
                    fh.write(line)
                    line = blif_file.readline()

            # parse the downloaded file
            blif = blifparser.BlifParser(f_name).blif

            # check .model, .inputs, .outputs
            self.assertEqual(blif.model.name, "comparatore2")
            self.assertEqual(blif.inputs.inputs, ["A1", "A0", "B1", "B0"])
            self.assertEqual(blif.outputs.outputs, ["O"])

            # check .search
            self.assertEqual(len(blif.imports), 1)
            self.assertEqual(blif.imports[0].filepath, "xnor.blif")

            # check .subckt
            self.assertEqual(len(blif.subcircuits), 2)
            self.assertEqual(blif.subcircuits[0].modelname, "xnor")
            self.assertEqual(blif.subcircuits[0].params, ["A=A1", "B=B1", "O=X1"])

            self.assertEqual(blif.subcircuits[1].modelname, "xnor")
            self.assertEqual(blif.subcircuits[1].params, ["A=A0", "B=B0", "O=X0"])

            # check .names
            self.assertEqual(len(blif.booleanfunctions), 1)
            self.assertEqual(blif.booleanfunctions[0].inputs, ["X1", "X0"])
            self.assertEqual(blif.booleanfunctions[0].output, "O")
            self.assertEqual(blif.booleanfunctions[0].truthtable, [['1', '1', '1']])

            # check number of occurrencies of keywords
            self.assertEqual(blif.nkeywords[".model"], 1)
            self.assertEqual(blif.nkeywords[".inputs"], 1)
            self.assertEqual(blif.nkeywords[".outputs"], 1)
            self.assertEqual(blif.nkeywords[".search"], 1)
            self.assertEqual(blif.nkeywords[".subckt"], 2)
            self.assertEqual(blif.nkeywords[".names"], 1)
            self.assertEqual(blif.nkeywords[".end"], 1)

            # there shouldn't be any problem in the file
            self.assertEqual(len(blif.problems), 0)

    def test_comparatore4(self):
        fileurl = baseurl + "comparatori/comparatore4.blif"

        # request the file
        blif_file = urllib.urlopen(fileurl)

        # create a temporary folder to download the file
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'tmp_file')

            # write the BLIF file to a local file
            with open(f_name, 'wb') as fh:
                line = blif_file.readline()
                while line.decode() != "":
                    fh.write(line)
                    line = blif_file.readline()

            # parse the downloaded file
            blif = blifparser.BlifParser(f_name).blif

            # check .model, .inputs, .outputs
            self.assertEqual(blif.model.name, "comparatore4")
            self.assertEqual(blif.inputs.inputs, ["A3", "A2", "A1", "A0", "B3", "B2", "B1", "B0"])
            self.assertEqual(blif.outputs.outputs, ["O"])

            # check .search
            self.assertEqual(len(blif.imports), 1)
            self.assertEqual(blif.imports[0].filepath, "xnor.blif")

            # check .subckt
            self.assertEqual(len(blif.subcircuits), 4)
            self.assertEqual(blif.subcircuits[0].modelname, "xnor")
            self.assertEqual(blif.subcircuits[0].params, ["A=A3", "B=B3", "O=X3"])

            self.assertEqual(blif.subcircuits[1].modelname, "xnor")
            self.assertEqual(blif.subcircuits[1].params, ["A=A2", "B=B2", "O=X2"])

            self.assertEqual(blif.subcircuits[2].modelname, "xnor")
            self.assertEqual(blif.subcircuits[2].params, ["A=A1", "B=B1", "O=X1"])

            self.assertEqual(blif.subcircuits[3].modelname, "xnor")
            self.assertEqual(blif.subcircuits[3].params, ["A=A0", "B=B0", "O=X0"])

            # check .names
            self.assertEqual(len(blif.booleanfunctions), 1)
            self.assertEqual(blif.booleanfunctions[0].inputs, ["X3", "X2", "X1", "X0"])
            self.assertEqual(blif.booleanfunctions[0].output, "O")
            self.assertEqual(blif.booleanfunctions[0].truthtable, [['1', '1', '1', '1', '1']])

            # check number of occurrencies of keywords
            self.assertEqual(blif.nkeywords[".model"], 1)
            self.assertEqual(blif.nkeywords[".inputs"], 1)
            self.assertEqual(blif.nkeywords[".outputs"], 1)
            self.assertEqual(blif.nkeywords[".search"], 1)
            self.assertEqual(blif.nkeywords[".subckt"], 4)
            self.assertEqual(blif.nkeywords[".names"], 1)
            self.assertEqual(blif.nkeywords[".end"], 1)

            # there shouldn't be any problem in the file
            self.assertEqual(len(blif.problems), 0)


if __name__ == "__main__":
    if have_internet():
        unittest.main()
    else:
        print("Can't test BlifParser(): there is no Internet")
