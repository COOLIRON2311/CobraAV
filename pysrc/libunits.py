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


class Hours(_Unit):
    _name = 'hours'

    def __init__(self, time: int) -> None:
        self._value = time * 3600
        super().__init__(time)


class Days(_Unit):
    _name = 'days'

    def __init__(self, time: int) -> None:
        self._value = time * 86400
        super().__init__(time)


class Weeks(_Unit):
    _name = 'weeks'

    def __init__(self, time: int) -> None:
        self._value = time * 604800
        super().__init__(time)


class Months(_Unit):
    _name = 'months'

    def __init__(self, time: int) -> None:
        self._value = time * 2592000
        super().__init__(time)


class Bytes(_Unit):
    _name = 'bytes'

    def __init__(self, size: int) -> None:
        self._value = size
        super().__init__(size)


class KBytes(_Unit):
    _name = 'kilobytes'

    def __init__(self, size: int) -> None:
        self._value = size * 1024
        super().__init__(size)
