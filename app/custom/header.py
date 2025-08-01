from dataclasses import dataclass
from typing import Any

from nicegui import ui
from nicegui.elements.drawer import Drawer


@dataclass
class TabInfo:
    name: str
    icon: str
    content: Any | None = None


class TabbedHeader(ui.header):
    def __init__(
        self,
        *,
        value: bool = True,
        title: str | None = None,
        tab_list: list[TabInfo] | None = None,
        opening_tab: str | None = None,
        drawer: Drawer | None = None,
        fixed: bool = True,
        bordered: bool = False,
        elevated: bool = False,
    ) -> None:
        """Tab navigation in header

        Inspired by https://github.com/zauberzeug/nicegui/discussions/1715#discussioncomment-7211915

        Uses tabs instead of button in headers.

        ```
        @router.page("/")
        async def editor_page():
            tab_list = [
                header.TabInfo("Tab 1", "home", rename_tab),
                header.TabInfo("Tab 2", "favorite", cbz_editor_tab),
            ]

            heading = header.TabbedHeader(
                title="My App",
                tab_list=tab_list,
            )

            def refresh_tab(e):
                tab = next(tab for tab in tab_list if tab.name == e.value)
                tab.content.refresh() # have the conent have `ui.refreshable` decorator

            with (
                ui.tab_panels()
                .classes("w-full")
                .bind_value(heading, "current_tab")
                .on_value_change(refresh_tab) # Add this if you need the tabs to refresh the content
            ):
                for tab in tab_list:
                    with ui.tab_panel(tab.name):
                        # have all tab content functions async if one of them needs async
                        await tab.content() if tab.content is not None else None
        ```

        Args:
            value (bool, optional): whether the header is already opened. Defaults to True.
            title (str | None, optional): ther the header should be fixed to the top of the page. Defaults to None.
            tab_list (list[TabInfo] | None, optional): list of tab and its content. Defaults to None.
            opening_tab (str | None, optional): name of the tab to open to. Defaults to None.
            drawer (Drawer | None, optional): drawer object (could be ui.left_drawer, ui.right_drawer, ui.drawer). Defaults to None.
            fixed (bool, optional): whether the header should be fixed to the top of the page. Defaults to True.
            bordered (bool, optional): whether the header should have a border. Defaults to False.
            elevated (bool, optional): whether the header should have a shadow. Defaults to False.

        """

        super().__init__(
            value=value,
            fixed=False,
            bordered=bordered,
            elevated=elevated,
            wrap=True,
            add_scroll_padding=True,
        )
        if fixed:
            self.props("reveal")
        self.classes(
            f"items-center px-2 {'pt-2 pb-2' if tab_list is None else 'pt-1 pb-0'}"
        )
        with self:
            if drawer is not None:
                ui.button(icon="menu", on_click=lambda: drawer.toggle()).props(
                    "flat color=white"
                )
            if title is not None:
                ui.label(title).classes(f"text-lg pl-{0 if drawer is not None else 5}")
            ui.space()
            if tab_list is not None:
                self.current_tab = (
                    opening_tab
                    if opening_tab is not None
                    and any(opening_tab == tab.name for tab in tab_list)
                    else tab_list[0].name
                )
                with ui.row():
                    with (
                        ui.tabs()
                        .classes("w-full max-sm:hidden")
                        .props("inline-label")
                        .bind_value(self, "current_tab")
                    ):
                        for tab in tab_list:
                            ui.tab(tab.name, label=tab.name, icon=tab.icon)

                    with (
                        ui.tabs()
                        .classes("w-full sm:hidden")
                        .bind_value(self, "current_tab")
                    ):
                        for tab in tab_list:
                            ui.tab(tab.name, label="", icon=tab.icon)
            ui.space()
