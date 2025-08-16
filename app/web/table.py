from typing import Any

from nicegui import APIRouter, ui

from app.custom import ssp_table

router = APIRouter(prefix="/table")


@router.page("/")
def page_2():
    rows = [
        {"name": "Noah", "age": 33},
        {"name": "Emma", "age": 21},
        {"name": "Rose", "age": 88},
        {"name": "James", "age": 59},
        {"name": "Olivia", "age": 62},
        {"name": "Liam", "age": 18},
    ]

    def fetch_rows_and_count(
        limit: int = 10, offset: int = 0, filter: str = ""
    ) -> tuple[list[dict[str, Any]], int]:
        new_rows = []
        if filter != "":
            for row in rows:
                if (filter.lower() in str(row["name"]).lower()) | (
                    filter in str(row["age"])
                ):
                    new_rows.append(row)
        else:
            new_rows = rows[:]
        if limit == 0:
            limit = len(new_rows)
            offset = 0
        return (new_rows[offset : (limit + offset)], len(new_rows))

    ui.label("Heter")
    table = ssp_table.Table(
        columns=[
            {
                "name": "name",
                "label": "Name",
                "field": "name",
                "align": "left",
                "sortable": True,
            },
            {
                "name": "age",
                "label": "Age",
                "field": "age",
                "align": "left",
                "sortable": True,
            },
        ],
        row_key="name",
        pagination=4,
        fetch_rows_and_count=fetch_rows_and_count,
    )
    ui.input("Search by name/age").bind_value(table, "filter")
