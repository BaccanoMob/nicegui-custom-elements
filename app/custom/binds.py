from dataclasses import field
from typing import Any

from nicegui import binding

# Some generic dataclass binds

@binding.bindable_dataclass
class TextBind:
    text: str | None

    def __init__(self, text: str | None = None) -> None:
        self.text = text

    def update(self, new_text: str) -> None:
        self.text = new_text


@binding.bindable_dataclass
class ProgressBind:
    value: float

    def __init__(self, value: float = -1) -> None:
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
        self.value = value

    def toggle(self) -> None:
        self.value = not self.value

    def on(self) -> None:
        self.value = True

    def off(self) -> None:
        self.value = False


@binding.bindable_dataclass
class ListBind:
    value: list[Any] = field(default_factory=list)

    def replace(self, new_value: list[Any]):
        self.value = new_value

    def append(self, element: Any):
        self.value.append(element)

    def clear(self):
        self.value = []
