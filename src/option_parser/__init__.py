"""
option_parser is a Python library for processing and retrieving command-line arguments in a simple, straightforward way. The library user will define what options
their program requires and option_parser will handle retrieving those options from `sys.argv`, validating option parameters, and if desired it will also handle
errors automatically.

# Example
The following code will print out the sum or product of the two given integers:

```python
from option_parser import Option, OptionParser

parser = OptionParser("Calculate the sum or product of the supplied arguments")
sum_option = Option("s", "sum")
sum_option.set_description("Returns the sum of x and y")
sum_option.set_parameter_settings(
    parameter_type = int,
    required = True,
    parameter_count = 2,
    metavar = ["x", "y"]
)

product_option = Option("p", "product")
product_option.set_description("Returns the product of x and y")
product_option.set_parameter_settings(
    parameter_type = int,
    required = True,
    parameter_count = 2,
    metavar = ["x", "y"]
)

parser.add_options(sum_option, product_option)

processed_options = parser.parse()

if(processed_options.is_set(sum_option)):
    sum_parameters = processed_options.get_option_parameter(sum_option)
    print(f"{sum_parameters[0] + sum_parameters[1]}")
if(processed_options.is_set(product_option)):
    product_parameters = processed_options.get_option_parameter(product_option)
    print(f"{product_parameters[0] * product_parameters[1]}")
```

If the code above was saved to a file called `calc.py`, then it can be run as follows:

```
> python calc.py -s 2 4
6
> python calc.py -p 2 4
8
> python calc.py -s 1 1 -p 2 3
2
6
> python calc.py -h
Calculate the sum or product of the supplied arguments

Options:
-s x y, --sum=x,y
        Returns the sum of x and y
-p x y, --product=x,y
        Returns the product of x and y
-h, --help
        Prints this help message and exits.
--
        Terminate option list.
```

# Usage
## Creating parser
Creating a parser is done simply by initializing an `option_parser.OptionParser` object. `option_parser.OptionParser` constructor takes two optional parameters:
`description` - program description to be displayed in the help page
`throw_on_error` - boolean flag to specify error handling behavior during parsing. If `False` (which it is by default), then the program will print error info, print help page, and exit. Otherwise it will raise exceptions.

```python
parser = OptionParser(description='This program will greet you using your name.')
```

## Creating an option
Each option is initially created and initialized as an `option_parser.option.Option` object. `option_parser.option.Option` constructor arguments are string flags to represent the given option (single-letter flags will be prefixed with `-`, longer flags will be prefixed with `--`).

Option description can then be set using the `option_parser.option.Option`'s `set_description(description)` method, option can be set to be required using `option_parser.option.Option`'s `set_as_required()` method,
and option can be allowed to accept parameters by calling `option_parser.option.Option`'s `set_parameter_settings()`.

```python
name_option = Option("n", "name")
name_option.set_description("Sets your name")
```

## Configuring option parameters
`option_parser.option.Option` can be configured to accept from 0 to N parameters. Parameters can be mandatory and non-mandatory, they can be cast to a certain type, and so on.
Parameter configuration is done using `option_parser.option.Option`'s `set_parameter_settings()` method. For example:

```python
vector_option = Option("v", "vector")
vector_option.set_description("Set a non-negative vector")

def vector_validator(num):
    return num >= 0

vector_option.set_parameter_settings(
    parameter_type = int,
    parameter_count = 2,
    required = True,
    metavar=["x", "y"],
    validator=vector_validator
)
```

The above code creates a `-v`, `--vector` option which has 2 mandatory int parameters. It also has a validator which verifies that the supplied parameters are greater than or equal to 0.
The `metavar` argument provides (in this case) a list of parameter placeholders to display in the program's help page. For single parameters, only a single string should be supplied.

## Adding options
Options are then added to the parser by calling the `option_parser.OptionParser`'s `add_options(option1, option2, ...)` method.

```python
name_option = Option('n', 'name')
name_option.set_description('Your name')
name_option.set_as_required()
name_option.set_parameter_settings(
    type=str,
    required=True,
    metavar='NAME'
)

formal_option = Option('f', 'formal')
formal_option.set_description('Use formal greeting')

parser.add_options(name_option, formal_option)
```

## Parsing
Finally, the parsing can begin. The following code will read sys.argv and process the received command-line arguments into a `option_parser.processed_options.ProcessedOptions` object.

```python
processed_options = parser.parse()
```

## Retrieving processed options and parameters
After processed_options is created, methods can be called on it to verify options' presence, whether parameters were supplied to those options and the parameters themselves.
Additionally, plain arguments can be retrieved as well.

```python
name = processed_options.get_option_parameter(name_option) # we do not have to verify whether name_option was supplied as it's mandatory
if(processed_options.is_set(formal_option)):
    print(f"Good day, {name}")
else:
    print(f"Yo, {name}!")
```

## Error handling
option_parser supports both automatic and manual error handling. Error handling configuration is supplied to `option_parser.OptionParser`'s constructor as the `throw_on_error` argument:

```python
parser = OptionParser(throw_on_error = True)
```

`throw_on_error` is False by default. In that case, automatic error handling is invoked and if any user input error is detected during parsing, option_parser
will print error details, the help page, and then exit. If `throw_on_error` is `True`, it raises one of the following exceptions:

`option_parser.exceptions.InvalidOptionException` if a mandatory option is missing, unrecognized option is supplied, etc.
`option_parser.exceptions.InvalidParameterException` if supplied parameter count is wrong, parameter type is wrong, or parameter validator fails.

Those exceptions are then left to the library user to handle.

# Supported option key formats
option_parser supports the following option key formats:

* Short key - `^[A-Za-z]$`
* Long key - `^[^ ][^ ]+$`

Program user may also specify multiple short keys with a single dash prefix, e.g.:

```program.py -abc```

where `-a` `-b` `-c` are all option keys.

Parameters are then passed as follows:

* Short key - `-o a b c`, meaning a space must be between option key and the first parameter, and then spaces between each parameter
* Long key - `--option=param1,param2,param3`, meaning an equals sign must precede the first parameter, and then commas between each parameter

"""

from .option_parser import OptionParser
from .option import Option