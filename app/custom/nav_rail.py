from typing import Literal, override

from nicegui import ui
from nicegui.events import ClickEventArguments, Handler


class List(ui.list):
    def __init__(self) -> None:
        """Drawer List

        Generic ui.list with full width
        """
        super().__init__()
        self.classes("w-full")

    def set_active_label(self, current_page: str):
        for child in self.descendants():
            if child.tag == "q-item-label":
                if child._text == current_page:
                    child.parent_slot.parent.parent_slot.parent.props("active")


class Item(ui.item):
    def __init__(
        self,
        label: str = "",
        icon: str | None = None,
        *,
        on_click: Handler[ClickEventArguments] | None = None,
    ) -> None:
        """Drawer Item

        Args:
            label (str, optional): text to be displayed on item. Defaults to "".
            icon (str | None, optional): icon to be displayed on item. If None, this item would not be displayed on the drawer. Defaults to None.
            on_click (Handler[ClickEventArguments] | None, optional): function to run when on clicked. Defaults to None.
        """
        super().__init__("", on_click=on_click)
        with self:
            with ui.item_section().props("avatar"):
                ui.icon(icon)
            with ui.item_section():
                ui.item_label(label)


class MiniDrawer(ui.drawer):
    def __init__(
        self,
        *,
        side: Literal["left", "right"] = "left",
        value: bool | None = None,
        fixed: bool = True,
        bordered: bool = False,
        elevated: bool = False,
        top_corner: bool = False,
        bottom_corner: bool = False,
    ) -> None:
        """Mini Drawer

        Based on https://github.com/zauberzeug/nicegui/discussions/4961#discussioncomment-13786468

        This version makes the mini mode on drawer feel more smoother.

        Example,

        ```
        with nav_rail.MiniDrawer(value=False):
            with nav_rail.List():
                nav_rail.Item(label="Nice Guy",icon="person"):
                nav_rail.Item(label="Mail",icon="inbox"):
        ```

        Args:
            side (Literal[&quot;left&quot;, &quot;right&quot;], optional): Specify the side the drawer should open. Defaults to "left".
            value (bool | None, optional): whether the drawer is already opened. If None, when layout width is above threshold drawer opens. Defaults to None.
            fixed (bool, optional): whether the drawer is fixed or scrolls with the content. Defaults to True.
            bordered (bool, optional): whether the drawer should have a border. Defaults to False.
            elevated (bool, optional): whether the drawer should have a shadow. Defaults to False.
            top_corner (bool, optional): whether the drawer expands into the top corner. Defaults to False.
            bottom_corner (bool, optional): whether the drawer expands into the bottom corner. Defaults to False.
        """
        super().__init__(
            side,
            value=value,
            fixed=fixed,
            bordered=bordered,
            elevated=elevated,
            top_corner=top_corner,
            bottom_corner=bottom_corner,
        )
        self.classes("p-0")
        self.props(add="overlay")
        self.on("mouseenter", lambda: self.props(remove="mini", add="overlay"))
        self.on("mouseleave", lambda: self.props(add="mini", remove="overlay"))

    @override
    def toggle(self) -> None:
        self.props(add="overlay", remove="mini")
        return super().toggle()
