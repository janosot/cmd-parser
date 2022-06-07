import pytest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidOptionException


def test_parser_exits_on_failure(mocker):
    # Arrange
    mocker.patch(
        "sys.argv",
        [
            "program",
            "-i"
        ]
    )

    # Act
    option_parser = OptionParser()

    # Assert
    with pytest.raises(SystemExit):
        option_parser.parse()    

