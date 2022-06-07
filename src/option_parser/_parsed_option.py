from typing import Iterable
from .option import Option

class _ParsedOption:
    def __init__(self, option: Option, option_parameters: Iterable[str]):
        self._option = option
        self._parameters = option_parameters
    
    def get_original_option(self) -> Option:
        return self._option

    def get_parameters(self) -> Iterable[str]:
        return self._parameters