# Command-line argument parsing library

option_parser is a Python library for processing and retrieving command-line arguments in a simple, straightforward way. The library user will define what options
their program requires and option_parser will handle retrieving those options from sys.argv, validating option parameters, and if desired it will also handle errors automatically.

## Installation
Python version >= 3.6 required.
From the root folder of the project run:

`pip3 install .`

## Tests
First run the following command from the root folder of the project:

`pip3 install -r requirements.txt`

Then:

`python -m pytest`

## Reference documentation
To generate the reference documentation (supplied as a webpage), first run:

`pip3 install -r requirements.txt`

Then:

`pdoc3 src/option_parser -o docs/ --html --force`

The reference documentation will then be generated in the docs/option_parser/ folder.

## Quickstart
```python
from option_parser import Option, OptionParser

parser = OptionParser("Prints given age to standard output")
age_option = Option("a", "age")
age_option.set_as_required()
age_option.set_description("Set age")
age_option.set_parameter_settings(
    parameter_type = int,
    required = True
)

parser.add_options(age_option)

processed_options = parser.parse()

print(processed_options.get_option_parameter(age_option))
```

More examples and detailed usage can be found in the reference documentation.
