from typing import Literal

from nicegui.element import Element


class Listener(Element):
    value: Literal["sm", "md", "lg", "xl", "2xl"] | None = None
    width: int = 0
    height: int = 0

    def __init__(
        self,
    ) -> None:
        """Resize Listener"""
        super().__init__(tag="q-resize-observer")
        self.on("resize", lambda e: self._on_resize(e.args))

    def _on_resize(self, size):
        self.width = size["width"]
        self.height = size["height"]
        breakpoints = {"sm": 640, "md": 768, "lg": 1024, "xl": 1280, "2xl": 1536}

        for prefix, min_width in breakpoints.items():
            if self.width >= min_width:
                self.value = prefix
            else:
                break
