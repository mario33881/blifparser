

class Search:

    def __init__(self, param):
        if not isinstance(param, str):
            raise TypeError("'{}' is not a string".format(param))

        self.filepath = param.strip()

        if self.filepath == "":
            raise ValueError(".search needs one parameter")

    def __repr__(self):
        """Object representation."""
        return "Search('" + self.filepath + "')"

    def __str__(self):
        """Printed string."""
        return ".search " + self.filepath


class Subckt:
    def __init__(self, params):
        if not isinstance(params, str):
            raise TypeError("'{}' is not a string".format(params))

        v_params = [param for param in params.split(" ") if param != ""]

        if len(v_params) < 2:
            raise ValueError(".subckt expects at least two parameters")

        self.modelname = v_params[0]
        self.params = v_params[1:]

        for param in self.params:
            if "=" not in param:
                raise ValueError("'{}' parameter is incorrect (there needs to be an equal sign '=')".format(param))

    def __repr__(self):
        """Object representation."""
        return "Subckt('" + self.modelname + " " + " ".join(self.params) + "')"

    def __str__(self):
        """Printed string."""
        return ".subckt " + self.modelname + " " + " ".join(self.params)
