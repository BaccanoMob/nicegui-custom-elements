from dataclasses import asdict, dataclass, is_dataclass
from typing import Literal

from nicegui import ui


@dataclass()
class AGColDef:
    field: str

    wrapText: bool = True
    autoHeight: bool = True

    headerName: str | None = None
    wrapHeaderText: bool = True
    autoHeaderHeight: bool = True
    headerTooltip: str | None = None

    hide: bool = False

    editable: bool = False
    singleClickEdit: bool = False

    checkboxSelection: bool = False
    headerCheckboxSelection: bool = False

    sortable: bool = False
    sort: Literal["asc", "desc"] | None = None

    rowDrag: bool = False

    resizable: bool = True

    pinned: bool | Literal["left", "right"] | None = None

    tooltipField: str | None = None
    tooltipValueGetter: str | None = None
    # tooltipValueGetter='(p) => "P value is " + p.value' # Dynamic
    # tooltipValueGetter='() => "Tooltip text about Sport should go here"' # Fixed

    def forGrid(self):
        colDef = asdict(self)
        colDef[":tooltipValueGetter"] = colDef.pop("tooltipValueGetter")
        return colDef


@dataclass
class AGTooltipConfig:
    tooltipMouseTrack: bool = False
    tooltipInteraction: bool = False
    tooltipShowDelay: int = 0
    tooltipHideDelay: int = 2000


class AGGrid(ui.aggrid):
    async def get_ordered_selection(self):
        selected = await self.get_selected_rows()
        if len(selected) > 1:
            ordered_row_data = await self.get_client_data()
            selected = [row for row in ordered_row_data if row in selected]
        return selected

    async def update_row_data(self, rowData):
        await self.run_grid_method("setGridOption", "rowData", rowData)

    async def deselect_selection(self):
        await self.run_grid_method("deselectAll")

    async def update_new_order(self):
        await self.update_row_data(await self.get_client_data())

    def get_primary_column(self):
        return self.primary_column

    def __init__(
        self,
        rowData: list,
        *,
        columnDefs: list[AGColDef] | None = None,
        selection: Literal["multiple", "single"] | None = None,
        drag: Literal["multiple", "single"] | None = None,
        hide_header: bool = False,
        tooltip_config: AGTooltipConfig | None = None,
        html_columns: list[int] = [],
        theme: str | None = "balham",
        auto_size_columns: bool = True,
    ) -> None:
        """AGGrid Wrapper Class

        This will only for nicegui 2.x or until 32.1.0 community version of aggrid is being used.

        Args:
            rowData (list): list of rows
            columnDefs (list[AGColDef] | None, optional): column definitions based on the keys in rowData. If None, columnsDefs autopopulates based on rowData. Defaults to None.
            selection (Literal["multiple", "single"] | None, optional): whether the rows should be selectable. Defaults to None.
            drag (Literal["multiple", "single"] | None, optional): whether the rows should be draggable. Defaults to None.
            hide_header (bool, optional): whether the header row should be kept hidden. Defaults to False.
            tooltip_config (AGTooltipConfig | None, optional): basic configuration for tooltips. Defaults to None.
            html_columns (list[int], optional): list of columns that should be rendered as HTML. Defaults to [].
            theme (str | None, optional): AG Grid theme. Defaults to "balham".
            auto_size_columns (bool, optional): whether to automatically resize columns to fit the grid width. Defaults to True.
        """
        if len(rowData) == 0 and columnDefs is None:
            raise ValueError(
                "rowData and columnDef both can not be empty at the same time."
            )

        if len(rowData) != 0 and is_dataclass(rowData[0]):
            rowData = [asdict(row) for row in rowData]

        if columnDefs is None:
            columnDefs = [AGColDef(field=col) for col in rowData[0].keys()]

        options = {
            "columnDefs": [colDef.forGrid() for colDef in columnDefs],
            "rowData": rowData,
            "stopEditingWhenCellsLoseFocus": True,
        }

        selection = (
            "multiple"
            if any(colDef.headerCheckboxSelection for colDef in columnDefs)
            else selection
        )
        # selected to `multiple` if headerCheṭckboxSelection is True for one column

        if selection in ("multiple", "single"):
            options["rowSelection"] = selection
            # auto selected to `single` if checkboxSelection is True for one column

        if drag == "single":
            options["rowDragManaged"] = True
        elif drag == "multiple":
            # `rowDragMultiRow` requires rowDragManaged and `rowSelection` to `multiple` to work
            options["rowDragMultiRow"] = True
            options["rowDragManaged"] = True
            options["rowSelection"] = "multiple"

        primary_col = 0
        # To use instead of row index
        # In case `rowDrag` is not set
        # In case no columns is `pinned`
        # Below config make sures it defaults to first column or first pinned column be primary
        if not any([col.rowDrag for col in columnDefs]):
            if any([col.pinned for col in columnDefs]):
                for ind, col in enumerate(columnDefs):
                    if col.pinned:
                        primary_col = ind
                        break

        if drag in ("multiple", "single"):
            columnDefs[primary_col].rowDrag = True

        self.primary_column: str = columnDefs[primary_col].field
        options[":getRowId"] = f"(params) => params.data.{self.primary_column}"

        if hide_header:
            options["headerHeight"] = 0

        if tooltip_config is not None:
            for key, value in asdict(tooltip_config).items():
                options[key] = value

        super().__init__(
            options,
            html_columns=html_columns,
            theme=theme,
            auto_size_columns=auto_size_columns,
        )
