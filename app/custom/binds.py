from dataclasses import field
from typing import Any, Generic, TypeVar

from nicegui import binding

T = TypeVar("T")


@binding.bindable_dataclass
class ListBind(Generic[T]):
    value: list[T] = field(default_factory=list)

    def replace(self, new_list: list[Any]):
        self.value = new_list

    def append(self, element: Any):
        self.value = self.value + [element]

    def extend(self, elements: list[Any]):
        self.value = self.value + elements

    def clear(self):
        self.value = []


@binding.bindable_dataclass
class TextBind:
    text: str | None

    def __init__(self, text: str | None = None) -> None:
        super.__init__()
        self.text = text

    def update(self, new_text: str) -> None:
        self.text = new_text


@binding.bindable_dataclass
class ProgressBind:
    value: float

    def __init__(self, value: float = -1) -> None:
        super.__init__()
        if value > 1:
            self.value = 1
        elif value < 0:
            self.value = -1
        else:
            self.value = value

    @property
    def visible(self):
        if self.value < 0:
            return False
        return True


@binding.bindable_dataclass
class BoolBind:
    value: bool

    def __init__(self, value: bool = False) -> None:
        super.__init__()
        self.value = value

    def toggle(self) -> None:
        self.value = not self.value

    def on(self) -> None:
        self.value = True

    def off(self) -> None:
        self.value = False
