from typing import Literal

from nicegui import ui


class DualPane(ui.grid):
    def __init__(
        self,
        left_percent: int = 50,
        breakpoint_prefix: Literal["sm", "md", "lg", "xl", "2xl"] = "lg",
    ) -> None:
        """Dual Pane

        This uses a ui.grid as a base to make an adaptive split on breakpoint else it will be a single column.

        Make sure this element has even children to make the UI look neat.

        Args:
            left_percent (int, optional): Percentage of the left side of the pane. Defaults to 50.
            breakpoint_prefix (Literal["sm", "md", "lg", "xl", "2xl"], optional): Breakpoint to split the column into 2 panes. Defaults to "lg".
        """
        super().__init__(rows=None, columns=None)
        self.classes(f"w-full {breakpoint_prefix}:grid-cols-[{left_percent}%,auto]")
