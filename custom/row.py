from nicegui import ui


class Center(ui.row):
    def __init__(self) -> None:
        """Center

        Uses ui.row to place the content in the center of the container.
        """
        super().__init__(wrap=True, align_items="center")
        self.classes(add="w-full justify-center")
