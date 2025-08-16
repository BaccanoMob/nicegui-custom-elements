from nicegui import app, ui

from app.web import sortable, table

## Adding routers
app.include_router(sortable.router)
app.include_router(table.router)


@ui.page("/")
def _():
    ui.button("sortable").on_click(lambda: ui.navigate.to("/sortable/"))


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=8000,
        reload=True,
        show=False,
        storage_secret="my_secret",  # SAME SECRET AS ABOVE
    )
