#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLIFPARSER: A simple parser for BLIF files
"""

__author__ = "Zenaro Stefano"

import os
import shutil
import re
import tempfile

try:
    from ._version import __version__  # noqa: F401

    from . import keywords
    from . import utils
    from . import graph

except (ImportError, ModuleNotFoundError):
    from _version import __version__  # noqa: F401

    import utils
    import keywords
    import graph


class BlifParser:

    def __init__(self, t_file):  # noqa: C901
        """
        Parses the <t_file> BLIF file.

        :param str t_file: input BLIF file
        """
        # prepare the input file
        prepared_file = self.prepare_file(t_file)

        self.blif = keywords.generic.Blif()

        is_boolfunc = False
        boolfunc_dontcare = False
        is_fsm = False
        is_model = False

        with open(prepared_file) as fin:
            line = fin.readline()
            i = 1

            while line != "":
                linestrip = line.strip()

                # get and remove the metadata from the current line
                metadata = re.match("@!(.*?)!@", linestrip)
                if metadata:
                    i = metadata.groups()[0].lstrip("meta:")

                linestrip = re.sub("@!(.*?)!@", "", linestrip)

                keyword = None
                params = None

                # get the keyword in the current line
                if linestrip.startswith("."):
                    is_boolfunc = False
                    keyword = linestrip.split(" ")[0].strip()

                    try:
                        params = " ".join(linestrip.split(" ")[1:]).strip()
                    except IndexError:
                        pass

                try:
                    if linestrip == "":
                        # skip empty lines
                        pass
                    elif keyword:
                        # found a keyword
                        if keyword == ".model":
                            is_model = True
                            self.blif.model = keywords.generic.Model(params)
                        elif keyword == ".inputs":
                            self.blif.inputs = keywords.generic.Inputs(params)
                        elif keyword == ".outputs":
                            self.blif.outputs = keywords.generic.Outputs(params)
                        elif keyword == ".search":
                            self.blif.imports.append(keywords.subfiles.Search(params))
                        elif keyword == ".names":
                            is_boolfunc = True
                            self.blif.booleanfunctions.append(keywords.generic.Names(params, boolfunc_dontcare))
                        elif keyword == ".latch":
                            self.blif.latches.append(keywords.generic.Latch(params))
                        elif keyword == ".subckt":
                            self.blif.subcircuits.append(keywords.subfiles.Subckt(params))
                        elif keyword == ".start_kiss":
                            self.blif.fsm.ispresent = True
                            is_fsm = True
                        elif keyword == ".i":
                            if not is_fsm:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected .i keyword: "
                                                          "needs to be between .start_kiss and .end_kiss keywords".format(i))
                            self.blif.fsm.i = keywords.fsm.I(params)
                        elif keyword == ".o":
                            if not is_fsm:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected .o keyword: "
                                                          "needs to be between .start_kiss and .end_kiss keywords".format(i))
                            self.blif.fsm.o = keywords.fsm.O(params)
                        elif keyword == ".s":
                            if not is_fsm:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected .s keyword: "
                                                          "needs to be between .start_kiss and .end_kiss keywords".format(i))
                            self.blif.fsm.s = keywords.fsm.S(params)
                        elif keyword == ".p":
                            if not is_fsm:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected .p keyword: "
                                                          "needs to be between .start_kiss and .end_kiss keywords".format(i))
                            self.blif.fsm.p = keywords.fsm.P(params)
                        elif keyword == ".r":
                            if not is_fsm:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected .r keyword: "
                                                          "needs to be between .start_kiss and .end_kiss keywords".format(i))
                            self.blif.fsm.r = keywords.fsm.R(params)
                        elif keyword == ".end_kiss":
                            if not is_fsm:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected end of fsm: "
                                                          "there needs to be a .start_kiss keyword "
                                                          "BEFORE the .end_kiss keyword".format(i))
                            is_fsm = False
                        elif keyword == ".exdc":
                            boolfunc_dontcare = True
                        elif keyword == ".code":
                            self.blif.fsm.statecodes.append(keywords.fsm.Code(params))
                        elif keyword == ".end":
                            if not is_model:
                                self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected end of model on line {}".format(i))
                            is_model = False

                        try:
                            self.blif.nkeywords[keyword] += 1
                        except KeyError:
                            self.blif.problems.append("[ERROR][LINE ~ {}] Invalid keyword: '{}'".format(i, keyword))

                    else:
                        # found transition/truth table
                        if is_boolfunc:
                            curr_boolfunc = self.blif.booleanfunctions[-1]
                            curr_boolfunc.truthtable.append([char for char in linestrip if char != " "])

                        elif is_fsm:
                            fsm = self.blif.fsm
                            fsm.transtable.append([el for el in linestrip.split(" ") if el != " "])

                        elif linestrip != "":
                            self.blif.problems.append("[ERROR][LINE ~ {}] Unexpected text: '{}'".format(i, linestrip))

                except Exception as e:
                    self.blif.problems.append("[PARSING ERROR][LINE ~ {}] ".format(i) + str(e))

                line = fin.readline()

        # if an FSM is present in the file, check if it is valid
        if self.blif.fsm.ispresent:
            try:
                self.blif.fsm.is_valid()
            except Exception as e:
                self.blif.problems.append("[FSM PROBLEM] " + str(e))

        # check if each boolean function is valid
        for boolfunc in self.blif.booleanfunctions:
            try:
                boolfunc.is_valid()
            except Exception as e:
                self.blif.problems.append("[BOOLEAN FUNCTION PROBLEM] " + str(e))

    def prepare_file(self, t_file):
        """
        Prepares the <t_file> file for parsing.

        First it makes a copy of the file in a temporary folder,
        then adds metadata in the file (line number),
        removes the comments and the newlines created with "\".

        :param str t_file: input file path
        :return str nonewlines: "ready to be parsed" file path
        """
        filepath = os.path.abspath(t_file)

        # create a copy of the file inside a temporary folder
        tmp_dir = tempfile.mkdtemp()
        tmp_filepath = os.path.join(tmp_dir, "example.blif")
        shutil.copyfile(filepath, tmp_filepath)

        # adds metadata, removes comments and newlines on keywords' params
        metadata = utils.add_metadata(tmp_filepath)
        nocomments = utils.remove_comments(metadata)
        nonewlines = utils.remove_params_newline(nocomments)

        return nonewlines

    def get_graph(self):
        return graph.parse_blif(self.blif)


def main():
    import sys

    print("")

    if len(sys.argv) == 2:
        filepath = os.path.abspath(sys.argv[1])
        blif = BlifParser(filepath).blif

        print("ISSUES LIST:\n")

        for problem in blif.problems:
            print(problem)

        print("")
        print("=" * 50)
        print("\nREPORT:\n")
        print("* {} issues found".format(len(blif.problems)))
    else:
        print("blifparser expects only one parameter: the input BLIF file path")


if __name__ == "__main__":
    main()
