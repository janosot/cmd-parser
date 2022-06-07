from typing import Any, Callable, Iterable, Union

class _ParameterSettings:
    def __init__(self, parameter_type: type, required: bool, metavar: Union[str, Iterable[str]], parameter_count: int, validator: Callable[[Any], bool]):
        self._type = parameter_type
        self._required = required
        self._metavar = metavar
        self._parameter_count = parameter_count
        self._validator = validator

    def get_type(self) -> type:
        return self._type

    def is_required(self) -> bool:
        return self._required
    
    def get_metavar(self) -> Union[str, Iterable[str]]:
        return self._metavar
    
    def get_parameter_count(self) -> int:
        return self._parameter_count

    def get_validator(self) -> Callable[[str], bool]:
        return self._validator