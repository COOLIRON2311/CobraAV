from abc import ABC, abstractmethod


class _Unit(ABC):
    _name: str
    _value: int
    _raw: int

    @abstractmethod
    def __init__(self, value: int) -> None:
        self._raw = value

    def pprint(self) -> str:
        return f'{self._raw} {self._name}'

    def __repr__(self) -> str:
        return str(self._value)

    @property
    def value(self) -> int:
        return self._value


class Minutes(_Unit):
    _name = 'minutes'

    def __init__(self, time: int) -> None:
        self._value = time * 60
        super().__init__(time)
