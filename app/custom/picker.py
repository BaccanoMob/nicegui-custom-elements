import os
from pathlib import Path

from nicegui import events, ui


class local_file_picker(ui.dialog):
    def __init__(
        self,
        directory: str,
        *,
        upper_limit: str | None = "",
        multiple: bool = False,
        show_hidden_files: bool = False,
        show_dir_only: bool = False,
        allow_file_ext: str | None = None,
        fallback_directory: str = "/",
        is_dark: bool = False,
    ) -> None:
        """Local File Picker

        This is a simple file picker that allows you to select a file from the local filesystem where NiceGUI is running.

        Adapted from https://github.com/zauberzeug/nicegui/blob/main/examples/local_file_picker/local_file_picker.py

        :param directory: The directory to start in.
        :param upper_limit: The directory to stop at (None: no limit, default: same as the starting directory).
        :param multiple: Whether to allow multiple files to be selected.
        :param show_hidden_files: Whether to show hidden files.
        :param show_dir_only: Whether to show only directories or include files along.
        :param allow_file_ext: Space separated file extension list that are allowed. For example ".png .jpg .jpeg .webp"
        :param fallback_directory: Fallback directory if `directory` does not exist (defaults to `/`).
        :param is_dark: Fallback directory if `directory` does not exist (defaults to `/`).
        """
        super().__init__()

        self.path = Path(directory).expanduser()
        if not self.path.exists():
            ui.notify(
                f"{self.path} does not exist. Defaulting to `{fallback_directory}`"
            )
            self.path = Path(fallback_directory).expanduser()
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(
                directory if upper_limit == "" else upper_limit
            ).expanduser()
        self.show_hidden_files: bool = show_hidden_files
        self.show_dir_only: bool = show_dir_only
        self.allow_file_ext: tuple[str, ...] = (
            ()
            if (allow_file_ext is None or self.show_dir_only)
            else tuple(allow_file_ext.split(" "))
        )

        with self, ui.card():
            self.grid = (
                ui.aggrid(
                    {
                        "columnDefs": [{"field": "name", "headerName": "File"}],
                        "rowSelection": "multiple" if multiple else "single",
                    },
                    html_columns=[0],
                )
                .classes("w-96")
                .on("cellDoubleClicked", self.handle_double_click)
            )
            with ui.row().classes("w-full justify-end"):
                ui.button("New Folder", on_click=self._handle_new_folder)
                ui.space()
                ui.button("Cancel", on_click=self.close).props("outline")
                ui.button("Ok", on_click=self._handle_ok)

        self.grid.classes(
            add="ag-theme-balham-dark" if is_dark else "ag-theme-balham",
            remove="ag-theme-balham ag-theme-balham-dark",
        )
        self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob("*"))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith(".")]
        if len(self.allow_file_ext) != 0:
            paths = [
                p for p in paths if (p.name.endswith(self.allow_file_ext) or p.is_dir())
            ]
        elif self.show_dir_only:
            paths = [p for p in paths if p.is_dir()]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options["rowData"] = [
            {
                "name": f"📁 <strong>{p.name}</strong>"
                if p.is_dir()
                else f"📄 {p.name}",
                "path": str(p),
            }
            for p in paths
        ]
        if (self.upper_limit is None and self.path != self.path.parent) or (
            self.upper_limit is not None and self.path != self.upper_limit
        ):
            self.grid.options["rowData"].insert(
                0,
                {
                    "name": "📁 <strong>..</strong>",
                    "path": str(self.path.parent),
                },
            )
        self.grid.update()

    def handle_double_click(self, e: events.GenericEventArguments) -> None:
        self.path = Path(e.args["data"]["path"])
        if self.path.is_dir():
            self.update_grid()
        else:
            self.submit([str(self.path)])

    async def _handle_new_folder(self):
        def on_click():
            dialog.close()
            try:
                new_path = os.path.join(str(self.path), i.value)
                os.mkdir(new_path)
                self.path = Path(new_path)
                self.update_grid()
            except Exception as e:
                ui.notify(f"Something went wrong!! ({e})")

        with ui.dialog(value=True) as dialog, ui.card():
            i = ui.input("Folder Name")
            ui.button("Ok", on_click=on_click)

    def filter_paths(self, path_list: list[str]):
        if len(self.allow_file_ext) != 0:
            return [
                path
                for path in path_list
                if path.endswith(self.allow_file_ext) and not Path(path).is_dir()
            ]
        return path_list

    async def _handle_ok(self):
        rows = await self.grid.get_selected_rows()
        if len(rows) == 0 or ".." in rows[0]["name"]:
            paths = self.filter_paths([str(self.path)])
        else:
            paths = self.filter_paths([r["path"] for r in rows])

        if len(paths) == 1:
            self.submit(paths[0])
        elif len(paths) > 1:
            self.submit(paths)
