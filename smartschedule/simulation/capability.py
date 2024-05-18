from typing import Self

from attrs import frozen


@frozen
class Capability:
    name: str
    type: str

    @classmethod
    def skill(cls, name: str) -> Self:
        return cls(name=name, type="SKILL")

    @classmethod
    def permission(cls, name: str) -> Self:
        return cls(name=name, type="PERMISSION")

    @classmethod
    def asset(cls, name: str) -> Self:
        return cls(name=name, type="ASSET")
