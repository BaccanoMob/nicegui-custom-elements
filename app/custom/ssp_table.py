from collections.abc import Callable
from typing import Any, Callable, Literal

from nicegui import events, ui
from nicegui.events import (
    Handler,
    TableSelectionEventArguments,
    ValueChangeEventArguments,
)


class Table(ui.table):
    def __init__(
        self,
        *,
        columns: list[dict] | None = None,
        column_defaults: dict | None = None,
        row_key: str = "id",
        title: str | None = None,
        selection: Literal[None, "single", "multiple"] = None,
        on_select: Handler[TableSelectionEventArguments] | None = None,
        on_pagination_change: Handler[ValueChangeEventArguments] | None = None,
        pagination: int | dict = 10,
        fetch_rows_and_count: Callable[
            [int, int, str], tuple[list[dict[str, Any]], int]
        ],
    ) -> None:
        """Server side pagination table

        Inspired by https://github.com/zauberzeug/nicegui/discussions/1903#discussioncomment-8251437

        While, the above comment showed with refreshables, it is possible without it as well (like with this element).

        Requires `fetch_rows_and_count` function to work.
        `fetch_rows_and_count` requires 3 args: limit (int), offset (int) and filter (str).
        It should return a list of rows (list[dict[str, Any]]) and the total rows (int).

        `pagination` is modified from ui.table to required parameter with default value as 10.
        `pagination` as None is removed since it disables pagination feature.

        `pagination` as 0 must be configured in `fetch_rows_and_count` to get all rows.
        Records per page dropdown option `All` in pagination equals 0.
        If not configured, you will get `No data available` in the table (as rows is empty with limit 0).

        Args:
            fetch_rows_and_count (Callable[ [int, int, str], tuple[list[dict[str, Any]], int] ]): function that fetches rows and total row count
            columns (list[dict], optional): list of column objects (defaults to the columns of the first row)
            column_defaults (dict, optional): optional default column properties
            row_key (str, optional): name of the column containing unique data identifying the row. Defaults to "id".
            title (str, optional): title of the table. Defaults to None.
            selection (Literal[None, "single", "multiple"], optional): selection type. Defaults to None.
            pagination (int | dict): a dictionary correlating to a pagination object or number of rows per page (default: `10`)
            on_select (Handler[TableSelectionEventArguments], optional): callback which is invoked when the selection changes. Defaults to None.
            on_pagination_change (Handler[ValueChangeEventArguments], optional): callback which is invoked when the pagination changes. Defaults to None.
        """
        self.fetch_rows_and_count = fetch_rows_and_count

        rows, total = fetch_rows_and_count(
            limit=pagination["rowsPerPage"]
            if isinstance(pagination, dict)
            else pagination,
            offset=0,
        )
        super().__init__(
            rows=rows,
            columns=columns,
            column_defaults=column_defaults,
            row_key=row_key,
            title=title,
            selection=selection,
            pagination=pagination,
            on_select=on_select,
            on_pagination_change=on_pagination_change,
        )

        self.filter: str = ""
        self.props["pagination"]["rowsNumber"] = total
        self.on("request", self.do_server_side_pagination)

    def do_server_side_pagination(self, e: events.GenericEventArguments):
        """function to get new rows `fetch_rows_and_count` via on pagination"""
        new_pagination = e.args["pagination"]

        limit = int(new_pagination.get("rowsPerPage"))
        offset = (int(new_pagination.get("page")) - 1) * limit
        rows, total = self.fetch_rows_and_count(limit, offset, self.filter)

        new_pagination["rowsNumber"] = total
        self.props["pagination"].update(new_pagination)
        self.update_rows(rows)
