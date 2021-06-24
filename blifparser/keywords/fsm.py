

class Fsm:
    def __init__(self):
        """
        Defines an Fsm() object.

        Attributes:
        * self.i: represents the .i keyword (number of inputs)
        * self.o: represents the .o keyword (number of outputs)
        * self.s: represents the .s keyword (number of unique states)
        * self.p: represents the .p keyword (number of state transitions)
        * self.r: represents the .r keyword (name of the reset state)
        * self.ispresent: True if an FSM is present in the blif file
        * self.transtable: list of lists (each row is a state transition)
            > Each row contains 4 elements: ["<inputs>", "<current_state>", "<next_state>", "<outputs>"]
        * self.statecodes: list of Code() objects (they represent .code keywords, state encodings)
        """
        self.i = None
        self.o = None
        self.s = None
        self.p = None
        self.r = None
        self.ispresent = False
        self.transtable = []
        self.statecodes = []

    def is_valid(self):
        """
        Validates all the elements present in an Fsm() object.
        """
        # Be sure that self.ispresent is kept boolean
        if not isinstance(self.ispresent, bool):
            raise TypeError("Something went wrong: self.ispresent should be boolean")

        # check if input and output are specified
        self.validate_i()
        self.validate_o()

        # Check transition table
        self.validate_transtable()

        # Check .p, .s, .r keywords
        self.validate_p()
        self.validate_s()
        self.validate_r()

        # Check .code keywords
        self.validate_codes()

        return True

    def validate_i(self):
        """
        Validates .i keyword: it needs to be set as an I() instance.
        """
        if self.i:
            if not isinstance(self.i, I):
                raise TypeError(".i must be I() instance")
        else:
            raise ValueError(".i must be set")

    def validate_o(self):
        """
        Validates .o keyword: it needs to be set as an O() instance.
        """
        if self.o:
            if not isinstance(self.o, O):
                raise TypeError(".o must be O() instance")
        else:
            raise ValueError(".o must be set")

    def validate_p(self):
        """
        Validates .p keyword: it is valid if it is a P() instance or if it is None.

        If it is set its parameter needs to be equal to the number of rows
        present in the transition table.
        """
        # if .p is not None check its instance
        if self.p:
            if not isinstance(self.p, P):
                raise TypeError(".p must be P() instance")

            # be sure that the num_terms are equal to the
            # number of rows of the transition table
            num_terms = int(self.p.num)
            if len(self.transtable) != num_terms:
                raise ValueError(".p <num-terms> has incorrect <num-terms> value "
                                 "(it should be '{}' instead of '{}' because the "
                                 "transition table has that amount of rows)".format(len(self.transtable), num_terms))

    def validate_s(self):
        """
        Validates .s keyword: it is valid if it is a S() instance or if it is None.

        If it is set its parameter needs to be equal to the number of unique states
        present in the transition table.
        """
        state_names = self.get_state_names()

        if self.s:
            if not isinstance(self.s, S):
                raise TypeError(".s must be S() instance")

            num_states = int(self.s.num)
            expected_num = len(state_names)
            if expected_num != num_states:
                raise ValueError(".s <num-states> has incorrect <num-states> value "
                                 "(it should be '{}' instead of '{}' because the transition "
                                 "table contains that amount of unique states)".format(expected_num, num_states))

    def validate_r(self):
        """
        Validates .r keyword: it is valid if it is a R() instance or if it is None.

        If it is set its parameter needs to be a state that is
        present in the transition table.
        """
        state_names = self.get_state_names()

        if self.r:
            if not isinstance(self.r, R):
                raise TypeError(".r must be R() instance")

            reset_state = self.r.name
            if reset_state not in state_names:
                raise ValueError(".r <reset-state> has incorrect <reset-state> value "
                                 "(can't find '{}' in the transition table)".format(reset_state))

    def validate_codes(self):
        """
        Validates .code keywords: it is valid if self.statecodes contains Code() instances.
        """
        if not isinstance(self.statecodes, list):
            raise TypeError("Something went wrong: statecodes is not a list")

        # be sure that self.statecodes only contain states
        for code in self.statecodes:
            if not isinstance(code, Code):
                raise TypeError(".code in statecodes must be Code() instance")

    def get_state_names(self):
        """
        Get unique state names from the transition table.
        """
        states = set()
        for row in self.transtable:
            if len(row) == 4:
                states.add(row[1])
                states.add(row[2])

        return states

    def validate_transtable(self):  # noqa: C901
        """
        Validates the transition table.

        The transition table:
        * needs to contain lists of strings (4 for each list)
        * be sure that the first element (inputs) is make of 0 1 -
        * be sure that the inputs are the amount specified by the .i keyword
        * be sure that the last element (outputs) is make of 0 1 -
        * be sure that the outputs are the amount specified by the .o keyword
        """

        if not isinstance(self.transtable, list):
            raise TypeError("Something went wrong: transition table is not a list")

        for row in self.transtable:
            # be sure that it contains lists of strings
            if not isinstance(row, list):
                raise TypeError("'{}' is not a list".format(row))

            for el in row:
                if not isinstance(el, str):
                    raise TypeError("'{}' in '{}' is not a string".format(el, row))

            # be sure that there are four strings inside each list
            if len(row) != 4:
                raise ValueError("'{}' row of the transition table doesn't have all the "
                                 "expected data (<input> <current-state> <next-state> <output>)".format(" ".join(row)))

            # be sure that the first element (inputs) is make of 0 1 -
            for el in row[0]:
                if el not in ["0", "1", "-"]:
                    raise ValueError("'{}' input of the '{}' row (transition table) "
                                     "has unexpected characters (accepted chars are "
                                     "['0', '1', '-'])".format(row[0], " ".join(row)))

            # be sure that the inputs are the amount specified by the .i keyword
            if len(row[0]) != int(self.i.num):
                raise ValueError("'{}' row (transition table) has an unexpected number "
                                 "of inputs (found {} elements in '{}' but expected {} "
                                 "based on the .i parameter)".format(" ".join(row), len(row[0]), row[0], self.i.num))

            # be sure that the last element (outputs) is make of 0 1 -
            for el in row[3]:
                if el not in ["0", "1", "-"]:
                    raise ValueError("'{}' output of the '{}' row (transition table) "
                                     "has unexpected characters (accepted chars are "
                                     "['0', '1', '-'])".format(row[3], " ".join(row)))

            # be sure that the outputs are the amount specified by the .o keyword
            if len(row[3]) != int(self.o.num):
                raise ValueError("'{}' row (transition table) has an unexpected number "
                                 "of outputs (found {} elements in '{}' but expected {} "
                                 "based on the .o parameter)".format(" ".join(row), len(row[3]), row[3], self.o.num))

    def __str__(self):
        """Printed string."""
        # be sure that the object is validated
        self.is_valid()

        # adds .start_kiss, .i, .o keywords for printing
        fsm = ".start_kiss\n"
        fsm += self.i.__str__() + "\n"
        fsm += self.o.__str__() + "\n"

        # adds .p, .s, .r keywords (if not None) for printing
        if self.p:
            fsm += self.p.__str__() + "\n"

        if self.s:
            fsm += self.s.__str__() + "\n"

        if self.r:
            fsm += self.r.__str__() + "\n"

        fsm += "\n"

        # adds the transition table for printing
        for row in self.transtable:
            fsm += " ".join(row) + "\n"

        fsm += "\n"

        # adds .end_kiss keyword for printing
        fsm += ".end_kiss\n"

        # adds the states encodings for printing
        for state in self.statecodes:
            fsm += state.__str__() + "\n"

        return fsm


class I:
    def __init__(self, params):
        """
        Defines .i keyword object.

        Validation steps:
        * params needs to be a string
        * params needs to be numeric (contain numbers)
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        try:
            int(params.strip())
        except ValueError:
            raise ValueError(".i parameter needs to be numeric (it must be made of digits 0-9)")

        self.num = params.strip()

    def __repr__(self):
        """Object representation."""
        return "I('" + self.num + "')"

    def __str__(self):
        """Printed string."""
        return ".i " + self.num


class O:
    def __init__(self, params):
        """
        Defines .o keyword object.

        Validation steps:
        * params needs to be a string
        * params needs to be numeric (contain numbers)
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        try:
            int(params.strip())
        except ValueError:
            raise ValueError(".o parameter needs to be numeric (it must be made of digits 0-9)")

        self.num = params.strip()

    def __repr__(self):
        """Object representation."""
        return "O('" + self.num + "')"

    def __str__(self):
        """Printed string."""
        return ".o " + self.num


class S:
    def __init__(self, params):
        """
        Defines .s keyword object.

        Validation steps:
        * params needs to be a string
        * params needs to be numeric (contain numbers)
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        try:
            int(params.strip())
        except ValueError:
            raise ValueError(".s parameter needs to be numeric (it must be made of digits 0-9)")

        self.num = params.strip()

    def __repr__(self):
        """Object representation."""
        return "S('" + self.num + "')"

    def __str__(self):
        """Printed string."""
        return ".s " + self.num


class P:
    def __init__(self, params):
        """
        Defines .p keyword object.

        Validation steps:
        * params needs to be a string
        * params needs to be numeric (contain numbers)
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        try:
            int(params.strip())
        except ValueError:
            raise ValueError(".p parameter needs to be numeric (it must be made of digits 0-9)")

        self.num = params.strip()

    def __repr__(self):
        """Object representation."""
        return "P('" + self.num + "')"

    def __str__(self):
        """Printed string."""
        return ".p " + self.num


class R:
    def __init__(self, params):
        """
        Defines .r keyword object.

        Validation steps:
        * params needs to be a string
        * params needs to contain one parameter with no spaces
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        self.name = params.strip()

        if " " in self.name or self.name == "":
            raise ValueError(".r accepts (and needs) only one parameter (the parameter can't contain spaces)")

    def __repr__(self):
        """Object representation."""
        return "R('" + self.name + "')"

    def __str__(self):
        """Printed string."""
        return ".r " + self.name


class Code:
    def __init__(self, params):
        """
        Defines .code keyword object.

        Validation steps:
        * params needs to be a string
        * params needs to contain two parameters separated by space(s)
        * the second parameter needs to contain zeros and ones only
        """
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        v_params = [param for param in params.split(" ") if param != ""]

        if len(v_params) != 2:
            raise ValueError(".code expects two parameters")

        self.state_name = v_params[0]
        self.state_encoding = v_params[1]

        for el in self.state_encoding:
            if el not in ["0", "1"]:
                raise ValueError("Unexpected char in the state encoding "
                                 "(only '0's and '1's are accepted): "
                                 ".code " + self.state_name + " " + self.state_encoding)

    def __repr__(self):
        """Object representation."""
        return "Code('" + self.state_name + " " + self.state_encoding + "')"

    def __str__(self):
        """Printed string."""
        return ".code " + self.state_name + " " + self.state_encoding
