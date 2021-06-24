# BLIFPARSER

This is a simple Python library that parses BLIF (Berkeley Logic Interchange Format) files (used by SIS, Sequential Interactive Synthesis).
> And also evalutes if some keyword's parameters have syntactically correct values.

Only the basic keywords are parsed (```.model```, ```.inputs```, ```.outputs```, ```.names```, all the FSM keywords, ```.latch```, ```.exdc```, ```.end```).
> More complex BLIF files with ```.clock```, ```.gate```, ```.mlatch```, ```.clock_event``` and delay constraits are only partially parsed.
>
> This is because the workflow I am supporting does not use these keywords

Currently only one ```.model``` keyword per file is supported.
> You can see this as a "feature" because it forces the use of a good practise: use many files, one per each component.

You can also use this library as a basic BLIF validator.
> Complex checks such as cross file definition checks and input-output names check are NOT implemented
> because the primary intent of this library is to parse BLIF files.

A more full/complex validator is in the works (and it will use this parser).

---
---

WARNING

This parser DOES NOT use grammar files NOR [PEG](https://en.wikipedia.org/wiki/Parsing_expression_grammar) for parsing blif files:

this means that the parsing could be "not perfect".
> If someone wants to contribute and change this feel free to make pull requests!
>
> If this library inspires you to write a better parser from scratch, please let me know by making a GH issue

This means that the library works because:
* the BLIF (format) is simple: most of the time parameters are on the same line of the keywords
* (some) unit and end to end tests were written

---
---

## Index

* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Description](#description)
* [Changelog](#changelog)
* [Author](#author)

## Requirements
* python 3

## Installation

First, install the library using PIP:

    pip install blifparser

Then:
* if you want to use this library as a validation tool, check the "[As a validator tool](#as-a-validator-tool)" section

* if you want to use this library inside your software, check the "[As a library](#as-a-library)" section
    > If this is the only way you want to use this software, you can also install it using the installer on the Github Release page

## Usage

## As a validator tool

Execute the script using this command:

    blifparser <input_path>

You can also execute it this way:

    python -m blifparser <input_path>

> Replace ```<input_path>``` with the path to the BLIF file to validate

When you have fixed the errors, execute the script until
you have fixed all the errors.
> Not all errors appear after the first script execution.

### As a library

Basic/common usage:
```py
# import the os library: useful to get the absolute path to the input file
import os
# import this library
import blifparser.blifparser as blifparser

# get the file path and pass it to the parser
filepath = os.path.abspath("example.blif")
parser = blifparser.BlifParser(filepath)

# get the object that contains the parsed data
# from the parser
blif = parser.blif
```

Now you can:

```py
# get the name of the model
print(blif.model.name)

# get the list of the inputs
print(blif.inputs.inputs)

# get the list of the outputs
print(blif.outputs.outputs)

# get the list of .search keyword
print(blif.imports)

# get the imported file name/path of the first .search keyword
first_import = blif.imports[0]
print(first_import.filepath)

# get the list of subcircuits (.subckt)
print(blif.subcircuits)

# get data from the first subcircuit definition
first_subcircuit = blif.subcircuits[0]
print(first_subcircuit.modelname)  # name of the model
print(first_subcircuit.params)     # subcircuit's parameters

# get the list of boolean functions (.names)
print(blif.booleanfunctions)

# get data from the first boolean function definition
first_boolfunc = blif.booleanfunctions[0]
print(first_boolfunc.inputs)      # list with the names of the inputs
print(first_boolfunc.output)      # string with the name of the output
print(first_boolfunc.truthtable)  # list of lists (each row is a truth table row)

# get the dictionary with the number of occurrencies of each keyword
print(blif.nkeywords)

# get the list of problems/issues
print(blif.problems)

# get the list of the latches
print(blif.latches)

# get the data of the first latch
first_latch = blif.latches[0]
print(first_latch.input)    # name of the input
print(first_latch.output)   # name of the output
print(first_latch.type)     # type of latch (like "re", ...)
print(first_latch.control)  # clock name
print(first_latch.initval)  # initial value

# get the data of the FSM (Finite State Machine)
print(blif.fsm.i.num)       # number of inputs
print(blif.fsm.o.num)       # number of outputs
print(blif.fsm.s.num)       # number of states
print(blif.fsm.p.num)       # number of state transitions
print(blif.fsm.r.name)      # name of the reset state
print(blif.fsm.transtable)  # list of lists (contains the transition table)
```

## Description

These are the first steps to use this library:
```py
# import the os library: useful to get the absolute path to the input file
import os
# import this library
import blifparser.blifparser as blifparser

# get the file path and pass it to the parser
filepath = os.path.abspath("example.blif")
parser = blifparser.BlifParser(filepath)

# get the object that contains the parsed data
# from the parser
blif = parser.blif
```

The ```blifparser.BlifParser()``` object is the parser:
it prepares the file for parsing using the ```prepare_file()``` method
and then creates a ```keywords.generic.Blif()``` object that will contain
all the information parsed from the file.
> The ```prepare_file()``` method copies the file and 
> then removes (on the copy): 
> * the newlines made with the backslash "```\```"
> * the comments made with "```#```".

Then each line is read and parsed:
* if the line contains a keyword, a "keyword" object is created and then
  "linked" to the ```keywords.generic.Blif()``` object (its parameters get parsed with the keyword)

    > For example: if a ```.model``` keyword is found, a ```keywords.generic.Model()``` object
    > gets created and set in the ```keywords.generic.Blif()``` object. (```keywords.generic.Blif().model```)

* if the line contains text and the line comes after the ```.names``` keyword
  it is interpreted as the truth table of the latest boolean function (defined by ```.names```)
    
    > This behavior stops when the next keyword is found

* if the line contains text and the line comes after the ```.start_kiss``` keyword
  it is interpreted as the transition table of the Finite State Machine.

    > This behavior stops when the next keyword is found

* If an unexpected text/keyword is found a "problem" or issue is collected inside the ```keywords.generic.Blif().problems``` list.

At the end of the parsing:
* if an FSM was found, a validation step checks if it is syntactically correct
* if some boolean functions were found, a validation step checks if they are syntactically correct
> The other validation steps are executed during object definition

Now you can use the ```blif``` object to get the parsed data
> Check the "Usage > [As a library](#as-a-library)" section for more details

## Changelog

**2021-04-23 1.0.0**:

First commit

## Author
[Zenaro Stefano (mario33881)](https://github.com/mario33881)
