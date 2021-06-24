#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def add_metadata(t_file):
    """
    Adds useful metadata to the file.

    Added metadata:
    * line number
    """
    tmp_dir = os.path.dirname(t_file)
    filename = os.path.basename(t_file)
    tmp_out = os.path.join(tmp_dir, filename + ".metadata.tmp")

    with open(tmp_out, "w") as fout:
        with open(t_file, "r") as fin:
            line = fin.readline()
            i = 1
            while line != "":
                metaline = "@!meta:{}!@".format(i) + line
                fout.write(metaline)
                i += 1
                line = fin.readline()

    return tmp_out


def remove_comments(t_file):
    """
    Removes comments from the file.
    """
    tmp_dir = os.path.dirname(t_file)
    filename = os.path.basename(t_file)
    tmp_out = os.path.join(tmp_dir, filename + ".nocomments.tmp")

    with open(tmp_out, "w") as fout:
        with open(t_file, "r") as fin:
            line = fin.readline()
            while line != "":
                not_commented = line.split("#")[0]
                fout.write(not_commented.strip())

                if not_commented.strip() != "":
                    fout.write("\n")

                line = fin.readline()

    return tmp_out


def remove_params_newline(t_file):
    """
    Removes newlines on parameters.
    """

    tmp_dir = os.path.dirname(t_file)
    filename = os.path.basename(t_file)
    tmp_out = os.path.join(tmp_dir, filename + ".nonewlines.tmp")

    with open(tmp_out, "w") as fout:
        with open(t_file, "r") as fin:
            line = fin.readline()
            while line != "":
                if line.strip().endswith("\\"):
                    nonewline = line.strip().replace("\\", " ")
                    fout.write(nonewline)
                else:
                    fout.write(line.strip() + "\n")

                line = fin.readline()

    return tmp_out
