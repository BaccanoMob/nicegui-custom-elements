from nicegui import APIRouter, ui
from app.custom.binds import ListBind
from app.custom import sortable


router = APIRouter(prefix="/examples")

@router.page("/sortable")
def sortable_example():
    @ui.refreshable
    def draw():
        def check_list():
            print(test.value)
            print("=" * 15)
            print(test2.value)
            print("=" * 15)

        class Custom(ui.card):
            def __init__(self, label: str) -> None:
                super().__init__(align_items=None)
                with self:
                    ui.label(label)

        def pop_test():
            try:
                # c1.clear()
                c1.pop(0)
                c1.update()
            except Exception as e:
                ui.notify(str(e))

        def insert_test():
            try:
                c2.insert(0, {"label": "Star"})
                c2.update()
            except Exception as e:
                ui.notify(str(e))

        def print_list():
            print(test.value)
            print(test2.value)

        ui.button("pop", on_click=pop_test)
        ui.button("insert", on_click=insert_test)
        ui.button("print", on_click=print_list)

        test = ListBind([{"label": str(i)} for i in range(3)])
        test2 = ListBind([{"label": str(i)} for i in range(20, 24)])

        ui.button("reset").on_click(draw.refresh)
        with ui.row():
            with ui.column():
                with ui.card():  # .classes("bg-red-200 p-0 size-64"):
                    c1 = sortable.Row(value=test.value, class_obj=Custom, group="a")

                with ui.card():  # .classes("bg-red-200 p-0 size-64"):
                    c2 = sortable.Column(value=test2.value, class_obj=Custom, group="a")

        ui.button("print", on_click=check_list)