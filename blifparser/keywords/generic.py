try:
    from . import fsm
except (ModuleNotFoundError, ImportError):
    import fsm


class Model:
    def __init__(self, modelname):
        """
        Defines a .model keyword object.

        Validation checks:
        * modelname needs to be a string
        * modelname needs to contain something (spaces are not accepted)
        """
        if not isinstance(modelname, str):
            raise TypeError("'{}' is not a string".format(modelname))

        self.name = modelname.strip()

        if " " in self.name or self.name == "":
            raise ValueError(".model accepts (and needs) only one parameter (the parameter can't contain spaces)")

    def __repr__(self):
        """Object representation."""
        return "Model('" + self.name + "')"

    def __str__(self):
        """Printed string."""
        return ".model " + self.name


class Inputs:
    def __init__(self, inputstring):
        """
        Defines a .inputs keyword object.

        Validation checks:
        * inputstring needs to be a string
            > inputs are separated by spaces
        """
        if not isinstance(inputstring, str):
            raise TypeError("'{}' is not a string".format(inputstring))

        self.inputs = [i for i in inputstring.split(" ") if i != ""]

        if len(self.inputs) == 0:
            raise ValueError(".inputs keyword expects at least one parameter")

    def __repr__(self):
        """Object representation."""
        return "Inputs('" + " ".join(self.inputs) + "')"

    def __str__(self):
        """Printed string."""
        return ".inputs " + " ".join(self.inputs)


class Outputs:
    def __init__(self, outputstring):
        """
        Defines a .outputs keyword object.

        Validation checks:
        * outputstring needs to be a string
            > outputs are separated by spaces
        """
        if not isinstance(outputstring, str):
            raise TypeError("'{}' is not a string".format(outputstring))

        self.outputs = [i for i in outputstring.split(" ") if i != ""]

        if len(self.outputs) == 0:
            raise ValueError(".outputs keyword expects at least one parameter")

    def __repr__(self):
        """Object representation."""
        return "Outputs('" + " ".join(self.outputs) + "')"

    def __str__(self):
        """Printed string."""
        return ".outputs " + " ".join(self.outputs)


class Names:
    def __init__(self, params, dontcare):
        """
        Defines a .names keyword object.

        Validation checks:
        * params needs to be a string
            > the last parameter in the string is the output
        * dontcare needs to be a boolean

        If dontcare is true, the output
        represents a don't care.
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        if not isinstance(dontcare, bool):
            raise TypeError("'{}' is not a boolean".format(dontcare))

        self.v_params = [param for param in params.split(" ") if param != ""]

        self.inputs = []
        self.truthtable = []
        self.output = None
        self.is_dontcare = dontcare

        if len(self.v_params) > 1:
            self.inputs = self.v_params[:-1]

        self.output = self.v_params[-1]

    def is_valid(self):  # noqa: C901
        """
        Validates data in the Names() object.

        Validation steps:

        """
        # be sure that self.inputs is a list of strings
        if not isinstance(self.inputs, list):
            raise TypeError("Something went wrong: self.inputs should be a list")

        for el in self.inputs:
            if not isinstance(el, str):
                raise TypeError("Something went wrong: '{}' self.inputs element should be a string".format(el))

        # be sure that self.output is a string
        if not isinstance(self.output, str):
            raise TypeError("Something went wrong: '{}' self.output should be a string".format(self.output))

        # be sure that self.is_dontcare stays a boolean
        if not isinstance(self.is_dontcare, bool):
            raise TypeError("Something went wrong: '{}' self.is_dontcare is not a boolean".format(self.is_dontcare))

        # validate the truth table
        if not isinstance(self.truthtable, list):
            raise TypeError("Something went wrong: self.truthtable should be a list")

        expected_el_num = len(self.inputs) + 1

        for row in self.truthtable:
            if not isinstance(row, list):
                raise TypeError("row '{}' is not a list (under '{}')".format(row, self.__str__()))

            for el in row:
                if not isinstance(el, str):
                    raise TypeError("'{}' element is not a string (in '{}' under '{}')".format(el, row, self.__str__()))

            formatted_row = "".join(row[:-1]) + " " + row[-1]
            if len(row) != expected_el_num:
                raise ValueError(
                    "'{}' row should have {} inputs + 1 output: found {} instead "
                    "(under '{}')".format(
                        formatted_row,
                        len(self.inputs),
                        len(row),
                        self.__str__()
                    )
                )

            for el in row[:-1]:
                if el not in ["0", "1", "-"]:
                    raise ValueError("Found unexpected char '{}' as input in row '{}' "
                                     "(under '{}'), only '1', '0' and '-' "
                                     "are accepted".format(el, formatted_row, self.__str__()))

            if row[-1] not in ["0", "1"]:
                raise ValueError("Found unexpected char '{}' as output in row '{}' "
                                 "(under '{}'), only '1' and '0' "
                                 "are accepted".format(el, formatted_row, self.__str__()))

        return True

    def __repr__(self):
        """Object representation."""
        return "Names('" + " ".join(self.inputs) + " " + self.output + "', " + str(self.is_dontcare) + ")"

    def __str__(self):
        """Printed string."""
        names = ""
        if self.is_dontcare:
            names = ".exdc\n"

        names += ".names " + " ".join(self.inputs) + " " + self.output

        if len(self.truthtable) > 0:
            names += "\n"
            for row in self.truthtable:
                formatted_row = "".join(row[:-1]) + " " + row[-1]
                names += formatted_row + "\n"

        return names


class Latch:
    def __init__(self, params):  # noqa: C901
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        self.v_params = [param for param in params.split(" ") if param != ""]

        self.problems = []
        self.input = None
        self.output = None
        self.type = None
        self.control = None
        self.initval = None

        # set the correct attributes based on the number of parameters
        if len(self.v_params) < 2:
            raise Exception("You need to specify at least an input and an output")

        elif len(self.v_params) == 2:
            self.problems.append(
                "WARNING: you should specify the initial value "
                "(otherwise you'll need to set it later using the set_state command)"
            )

        elif len(self.v_params) == 3:
            self.initval = self.v_params[2]

        elif len(self.v_params) == 4:
            self.type = self.v_params[2]
            self.control = self.v_params[3]

        elif len(self.v_params) == 5:
            self.type = self.v_params[2]
            self.control = self.v_params[3]
            self.initval = self.v_params[4]

        elif len(self.v_params) > 5:
            raise Exception("Too many parameters (correct usage is: .latch <input> <output> [<type> <control>] [<init-val>])")

        # set as values the parameters that must be specified
        self.input = self.v_params[0]
        self.output = self.v_params[1]

        # check if parameters have correct values

        if self.type:
            if self.type not in ["fe", "re", "ah", "al", "as"]:
                raise ValueError("<type> should be one of these values: ['fe', 're', 'ah', 'al', 'as']")

        if self.initval:
            if self.initval not in ["0", "1", "2", "3"]:
                raise ValueError("<init-val> should be one of these values: ['0', '1', '2', '3']")

    def __repr__(self):
        """Object representation."""
        latch = "Latch('"

        if len(self.v_params) == 2:
            latch += self.input + " " + self.output
        elif len(self.v_params) == 3:
            latch += self.input + " " + self.output + " " + self.initval
        elif len(self.v_params) == 4:
            latch += self.input + " " + self.output + " " + self.type + " " + self.control
        else:
            latch += self.input + " " + self.output + " " + self.type + " " + self.control + " " + self.initval

        latch += "')"
        return latch

    def __str__(self):
        """Printed string."""
        latch = ".latch "

        if len(self.v_params) == 2:
            latch += self.input + " " + self.output
        elif len(self.v_params) == 3:
            latch += self.input + " " + self.output + " " + self.initval
        elif len(self.v_params) == 4:
            latch += self.input + " " + self.output + " " + self.type + " " + self.control
        else:
            latch += self.input + " " + self.output + " " + self.type + " " + self.control + " " + self.initval

        return latch


class Blif:
    def __init__(self):
        self.model = None
        self.inputs = None
        self.outputs = None
        self.fsm = fsm.Fsm()
        self.imports = []
        self.subcircuits = []
        self.latches = []
        self.booleanfunctions = []
        self.problems = []

        self.nkeywords = {
            ".model": 0,
            ".inputs": 0,
            ".outputs": 0,
            ".search": 0,
            ".subckt": 0,
            ".latch": 0,
            ".names": 0,
            ".end": 0,
            ".start_kiss": 0,
            ".i": 0,
            ".o": 0,
            ".s": 0,
            ".p": 0,
            ".r": 0,
            ".end_kiss": 0,
            ".default_input_arrival": 0,
            ".default_output_required": 0,
            ".default_input_drive": 0,
            ".default_output_load": 0,
            ".default_max_input_load": 0,
            ".latch_order": 0,
            ".code": 0,
            ".exdc": 0
        }

    def __str__(self):
        """Printed string."""
        blif = self.model.__str__() + "\n"
        blif += self.inputs.__str__() + "\n"
        blif += self.outputs.__str__() + "\n"
        blif += "\n"

        if self.fsm.ispresent:
            blif += self.fsm.__str__() + "\n"
        else:
            for imported_file in self.imports:
                blif += imported_file.__str__() + "\n"

            for circuit in self.subcircuits:
                blif += circuit.__str__() + "\n"

            for latch in self.latches:
                blif += latch.__str__() + "\n"

            for function in self.booleanfunctions:
                blif += function.__str__() + "\n"

        blif += ".end\n"

        return blif
