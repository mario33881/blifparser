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


class TestFsm(unittest.TestCase):

    def test_arc6_202021_fsm(self):
        fileurl = "https://raw.githubusercontent.com/arc6-202021/lib_componenti_sis/"
        fileurl += "f831de9f16dacf4db13f9d9eebb335ee596c5e92/"
        fileurl += "fsm/controllore.blif"

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
            self.assertEqual(blif.model.name, "Controllore")
            self.assertEqual(
                blif.inputs.inputs,
                ["BANCOMAT_INSERITO", "CIFRA4", "CIFRA3", "CIFRA2", "CIFRA1", "CASH_OK"]
            )

            self.assertEqual(
                blif.outputs.outputs,
                ["REINSERIRE_CODICE", "ABILITAZIONE_EROGAZIONE", "BLOCCO_BANCOMAT", "CHECK_DISPONIBILITA"]
            )

            # check FSM
            self.assertTrue(blif.fsm.ispresent)
            self.assertEqual(blif.fsm.i.num, "6")
            self.assertEqual(blif.fsm.o.num, "4")
            self.assertEqual(blif.fsm.s.num, "19")
            self.assertEqual(blif.fsm.p.num, "57")
            self.assertEqual(blif.fsm.r.name, "INSERIMENTO")

            # check FSM transition table
            self.assertEqual(len(blif.fsm.transtable), 57)
            self.assertEqual(blif.fsm.transtable[0], ["0-----", "INSERIMENTO", "INSERIMENTO", "0000"])

            # check number of occurrencies of keywords
            self.assertEqual(blif.nkeywords[".model"], 1)
            self.assertEqual(blif.nkeywords[".inputs"], 1)
            self.assertEqual(blif.nkeywords[".outputs"], 1)
            self.assertEqual(blif.nkeywords[".start_kiss"], 1)
            self.assertEqual(blif.nkeywords[".i"], 1)
            self.assertEqual(blif.nkeywords[".o"], 1)
            self.assertEqual(blif.nkeywords[".s"], 1)
            self.assertEqual(blif.nkeywords[".p"], 1)
            self.assertEqual(blif.nkeywords[".r"], 1)
            self.assertEqual(blif.nkeywords[".end_kiss"], 1)
            self.assertEqual(blif.nkeywords[".search"], 0)
            self.assertEqual(blif.nkeywords[".subckt"], 0)
            self.assertEqual(blif.nkeywords[".names"], 0)
            self.assertEqual(blif.nkeywords[".end"], 1)

            # there shouldn't be any problem in the file
            self.assertEqual(len(blif.problems), 0)


if __name__ == "__main__":
    if have_internet():
        unittest.main()
    else:
        print("Can't test BlifParser(): there is no Internet")
