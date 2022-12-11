import networkx as nx

try:
    from . import blifparser
except (ImportError, ModuleNotFoundError):
    import blifparser


class Graph:
    def __init__(self, nx_graph, longest_label, max_inputs):
        """
        Memorizes the networkx graph, 
        the longest_label length, and the max_inputs number.
        """
        self.nx_graph = nx_graph
        self.longest_label = longest_label
        self.max_inputs = max_inputs


class Node:
    progressive_id = 1  # makes sure that each id is unique
    def __init__(self):
        """
        Defines a node.

        A node has:
        * a type: input, output, boolean_function, latch
        * an id: identifies the node in a graph
        > Note: the id is a progressive integer. 
        > The variable that controls that progressive integer is shared between Node instances.

        A node can have:
        * many inputs
        * many outputs

        """
        self.inputs = []
        self.outputs = []
        self.type = None
        self.id = Node.progressive_id
        self.node_color = "black"

        Node.progressive_id += 1  # makes sure that each id is unique
    
    def __str__(self) -> str:
        """
        Returns the Node's id as a string
        """
        return str(self.id)


def parse_blif(t_blif):
    """
    Parses a Blif obect to create a graph.
    """
    # prepare nodes objects
    nodes = make_nodes(t_blif)

    # add the nodes to a directed graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    # connect nodes together and keep some statistics
    longest_label = 1
    max_inputs = 1
    for n1 in nodes:
        for n2 in nodes:
            for n1_output in n1.outputs:
                for n2_input in n2.inputs:
                    if n1_output == n2_input:
                        # n1 --> n2
                        G.add_edge(n1, n2, label=n1_output)

                # save stats to scale the image
                if len(n1.inputs) > max_inputs:
                    max_inputs = len(n1.inputs)

                if len(n1_output) > longest_label:
                    longest_label = len(n1_output)

    return Graph(G, longest_label, max_inputs)


def make_nodes(t_blif):
    """
    Creates nodes that are not binded to each other
    but with the necessary information to bind them later.

    TODO: maybe divide this into 5 functions? (one for each type of node)
    """
    nodes = []

    # blif inputs (.inputs) are nodes that have one output: the input value
    for input in t_blif.inputs.inputs:
        n = Node()
        n.outputs.append(input)
        n.type = "input"
        n.parent = None
        n.name = str(n.id)
        n.node_color = "red"
        nodes.append(n)
    
    # blif outputs (.outputs) are nodes that have one input: the output value
    for output in t_blif.outputs.outputs:
        n = Node()
        n.inputs.append(output)
        n.type = "output"
        n.parent = None
        n.name = str(n.id)
        n.node_color = "blue"
        nodes.append(n)

    # blif boolean functions, defined using .names arg1 arg2 ...
    # have one output and might have multiple inputs
    for function in t_blif.booleanfunctions:
        n = Node()

        # collect the inputs
        for input in function.inputs:
            n.inputs.append(input)
        
        n.outputs.append(function.output)
        n.type = "boolean_function"
        n.parent = None
        n.name = str(n.id)
        nodes.append(n)
    
    # blif latches (.latch) have one input and one output
    for latch in t_blif.latches:
        n = Node()
        n.inputs.append(latch.input)
        n.outputs.append(latch.output)
        n.type = "latch"
        n.parent = None
        n.name = str(n.id)
        nodes.append(n)
    
    # blif sub-circuits (.subckt) might have multiple inputs and/or multiple outputs.
    # > to distinguish inputs from outputs it is necessary to parse imported (.search) modules
    for subckt in t_blif.subcircuits:
        n = Node()
        
        # loop for each imported file
        for imported_blif in t_blif.imports:
            filepath = imported_blif.filepath
            parser = blifparser.BlifParser(filepath)
            subckt_data = parser.blif

            # check if we have found the .model referenced by .subckt
            if subckt.modelname == subckt_data.model.name:
                # loop for each input (.inputs) of the .model inside the .search-ed file
                for model_input in subckt_data.inputs.inputs:
                    # loop for each parameter of .subckt
                    for subckt_param in subckt.params:
                        subckt_input = subckt_param.split("=")[0]
                        # if the .subckt parameter is also a .model input (of the imported file)
                        # that means that the parameter is an input of the sub-circuit
                        if model_input == subckt_input:
                            n.inputs.append(subckt_param.split("=")[1])
                
                # loop for each output (.outputs) of the .model inside the .search-ed file
                for model_output in subckt_data.outputs.outputs:
                    # loop for each parameter of .subckt
                    for subckt_param in subckt.params:
                        subckt_output = subckt_param.split("=")[0]
                        # if the .subckt parameter is also a .model output (of the imported file)
                        # that means that the parameter is an output of the sub-circuit
                        if model_output == subckt_output:
                            n.outputs.append(subckt_param.split("=")[1])
        
        n.type = "subckt"
        n.parent = None
        n.name = str(n.id)
        nodes.append(n)

    return nodes


if __name__ == "__main__":
    a = Node()
    print("A: ", a.__dict__)

    b = Node()
    print("B: ", b.__dict__)
    print("A: ", a.__dict__)

    c = Node()
    print("C: ", c.__dict__)
    print("B: ", b.__dict__)
    print("A: ", a.__dict__)
