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


class TestDatapath(unittest.TestCase):

    def test_arc6_202021_datapath(self):
        fileurl = "https://raw.githubusercontent.com/arc6-202021/lib_componenti_sis/"
        fileurl += "f831de9f16dacf4db13f9d9eebb335ee596c5e92/"
        fileurl += "datapath/datapath.blif"

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
            self.assertEqual(blif.model.name, "datapath")
            self.assertEqual(
                blif.inputs.inputs,
                [
                    "CASH_RICHIESTO9", "CASH_RICHIESTO8", "CASH_RICHIESTO7", "CASH_RICHIESTO6", "CASH_RICHIESTO5",
                    "CASH_RICHIESTO4", "CASH_RICHIESTO3", "CASH_RICHIESTO2", "CASH_RICHIESTO1", "CASH_RICHIESTO0",
                    "CASH_DISPONIBILE15", "CASH_DISPONIBILE14", "CASH_DISPONIBILE13", "CASH_DISPONIBILE12",
                    "CASH_DISPONIBILE11", "CASH_DISPONIBILE10", "CASH_DISPONIBILE9", "CASH_DISPONIBILE8",
                    "CASH_DISPONIBILE7", "CASH_DISPONIBILE6", "CASH_DISPONIBILE5", "CASH_DISPONIBILE4",
                    "CASH_DISPONIBILE3", "CASH_DISPONIBILE2", "CASH_DISPONIBILE1",
                    "CASH_DISPONIBILE0", "CHECK_DISPONIBILITA"
                ]
            )

            self.assertEqual(
                blif.outputs.outputs,
                [
                    "CASH_DA_EROGARE9", "CASH_DA_EROGARE8", "CASH_DA_EROGARE7", "CASH_DA_EROGARE6", "CASH_DA_EROGARE5",
                    "CASH_DA_EROGARE4", "CASH_DA_EROGARE3", "CASH_DA_EROGARE2", "CASH_DA_EROGARE1", "CASH_DA_EROGARE0",
                    "CASH_OK"
                ]
            )

            # check .search
            self.assertEqual(len(blif.imports), 5)
            self.assertEqual(blif.imports[0].filepath, "mux2i10b.blif")
            self.assertEqual(blif.imports[1].filepath, "mux2i16b.blif")
            self.assertEqual(blif.imports[2].filepath, "shiftersx16b.blif")
            self.assertEqual(blif.imports[3].filepath, "minoreuguale16.blif")
            self.assertEqual(blif.imports[4].filepath, "comparatore16.blif")

            # check .subckt (TODO: 2/7 .subckt are currently tested... )
            self.assertEqual(len(blif.subcircuits), 7)
            self.assertEqual(blif.subcircuits[0].modelname, "mux2i10b")
            self.assertEqual(
                blif.subcircuits[0].params,
                [
                    "S=CHECK_DISPONIBILITA_IN", "A9=N_ZERO", "A8=N_ZERO", "A7=N_ZERO", "A6=N_ZERO",
                    "A5=N_ZERO", "A4=N_ZERO", "A3=N_ZERO", "A2=N_ZERO", "A1=N_ZERO",
                    "A0=N_ZERO", "B9=CASH_RICHIESTO9", "B8=CASH_RICHIESTO8", "B7=CASH_RICHIESTO7", "B6=CASH_RICHIESTO6",
                    "B5=CASH_RICHIESTO5", "B4=CASH_RICHIESTO4", "B3=CASH_RICHIESTO3",
                    "B2=CASH_RICHIESTO2", "B1=CASH_RICHIESTO1", "B0=CASH_RICHIESTO0",
                    "O9=TM2_9", "O8=TM2_8", "O7=TM2_7", "O6=TM2_6", "O5=TM2_5",
                    "O4=TM2_4", "O3=TM2_3", "O2=TM2_2", "O1=TM2_1", "O0=TM2_0"
                ]
            )

            self.assertEqual(blif.subcircuits[1].modelname, "shiftersx16b")
            self.assertEqual(
                blif.subcircuits[1].params,
                [
                    "A14=N_ZERO", "A13=N_ZERO", "A12=N_ZERO", "A11=N_ZERO", "A10=N_ZERO",
                    "A9=TM2_9", "A8=TM2_8", "A7=TM2_7", "A6=TM2_6", "A5=TM2_5",
                    "A4=TM2_4", "A3=TM2_3", "A2=TM2_2", "A1=TM2_1", "A0=TM2_0",
                    "O15=IGNORE", "O14=M2_14", "O13=M2_13", "O12=M2_12", "O11=M2_11",
                    "O10=M2_10", "O9=M2_9", "O8=M2_8", "O7=M2_7", "O6=M2_6",
                    "O5=M2_5", "O4=M2_4", "O3=M2_3", "O2=M2_2", "O1=M2_1",
                    "O0=M2_0"
                ]
            )

            # check .latch
            self.assertEqual(len(blif.latches), 1)
            self.assertEqual(blif.latches[0].input, "CHECK_DISPONIBILITA")
            self.assertEqual(blif.latches[0].output, "CHECK_DISPONIBILITA_IN")
            self.assertEqual(blif.latches[0].type, "re")
            self.assertEqual(blif.latches[0].control, "NIL")
            self.assertEqual(blif.latches[0].initval, "0")

            # check .names
            self.assertEqual(len(blif.booleanfunctions), 2)
            self.assertEqual(blif.booleanfunctions[0].inputs, [])
            self.assertEqual(blif.booleanfunctions[0].output, "N_ZERO")
            self.assertEqual(blif.booleanfunctions[0].truthtable, [])

            self.assertEqual(blif.booleanfunctions[1].inputs, ["M4_le_CDS", "M4_eq_CDS"])
            self.assertEqual(blif.booleanfunctions[1].output, "CASH_OK")
            self.assertEqual(blif.booleanfunctions[1].truthtable, [["1", "0", "1"]])

            # check number of occurrencies of keywords
            self.assertEqual(blif.nkeywords[".model"], 1)
            self.assertEqual(blif.nkeywords[".inputs"], 1)
            self.assertEqual(blif.nkeywords[".outputs"], 1)
            self.assertEqual(blif.nkeywords[".search"], 5)
            self.assertEqual(blif.nkeywords[".subckt"], 7)
            self.assertEqual(blif.nkeywords[".names"], 2)
            self.assertEqual(blif.nkeywords[".end"], 1)

            # there shouldn't be any problem in the file
            self.assertEqual(len(blif.problems), 0)


if __name__ == "__main__":
    if have_internet():
        unittest.main()
    else:
        print("Can't test BlifParser(): there is no Internet")
