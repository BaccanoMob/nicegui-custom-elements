import random

from nicegui import APIRouter, ui

from app.custom import sortable
from app.custom.binds import ListBind

router = APIRouter(prefix="/examples")


class Custom(ui.card):
    def __init__(self, label: str) -> None:
        super().__init__(align_items=None)
        with self:
            ui.label(label)


@ui.refreshable
def draw():
    def pop_test():
        try:
            sort1.pop(0)
            sort1.update()
        except Exception as e:
            ui.notify(str(e))

    def insert_test():
        sort2.insert(0, {"label": f"{random.randint(0, 100)}"})
        sort2.update()

    list1 = ListBind([{"label": str(i)} for i in range(3)])
    list2 = ListBind([{"label": str(i)} for i in range(20, 24)])
    list3 = ListBind([{"label": str(i)} for i in range(30, 34)])
    list4 = ListBind([{"label": str(i)} for i in range(0, 15)])

    with ui.row():
        with ui.column():
            with ui.row():
                with ui.card():
                    ui.label("sort1")
                    sort1 = sortable.Row(value=list1.value, class_obj=Custom, group="a")

                with ui.card():
                    ui.label("sort2")
                    sort2 = sortable.Column(
                        value=list2.value, class_obj=Custom, group="a"
                    )

                with ui.card().classes(
                    "bg-red-100"
                ):  # .classes("size-24 h-fit min-h-24"):
                    ui.label("sort3")
                    sort3 = sortable.Column(
                        value=list3.value, class_obj=Custom, align_items="center"
                    ).classes("w-full h-fit min-h-12 p-1")

            with ui.card().classes("bg-green-100"):
                ui.label("sort4")
                sort4 = sortable.Grid(value=list4.value, class_obj=Custom, columns=4)

        ui.splitter()

        with ui.column():
            ui.label("sort1 & sort2 are in same group, while sort3 & sort4 are not.")

            ui.label("Show list contents:")
            with ui.row():
                ui.button("list1", on_click=lambda: ui.notify(list1.value))
                ui.button("list2", on_click=lambda: ui.notify(list2.value))
                ui.button("list3", on_click=lambda: ui.notify(list3.value))
                ui.button("list4", on_click=lambda: ui.notify(list4.value))

            ui.label("Show sortable contents:")
            with ui.row():
                ui.button("sort1", on_click=lambda: ui.notify(sort1.value))
                ui.button("sort2", on_click=lambda: ui.notify(sort2.value))
                ui.button("sort3", on_click=lambda: ui.notify(sort3.value))
                ui.button("sort4", on_click=lambda: ui.notify(sort4.value))

            ui.label("Pop/Insert via function (into sort1/sort2)")

            with ui.row():
                ui.button("pop", on_click=pop_test)
                ui.button("insert", on_click=insert_test)

            ui.label("Reset with refresh()")
            ui.button("reset").on_click(draw.refresh)


@router.page("/sortable")
def sortable_example():
    draw()


class TrelloCard(ui.card):
    def __init__(self, *, label: str) -> None:
        super().__init__(align_items=None)
        with self.classes("w-full"):
            ui.label(label)
            with ui.context_menu():
                ui.menu_item("Delete", on_click=self._delete_card)

    def _delete_card(self):
        data = self.parent_slot.parent.pop(
            self.parent_slot.parent.default_slot.children.index(self)
        )
        ui.notify(f"{data['label']} deleted!!", type="warning")


# https://github.com/zauberzeug/nicegui/pull/4819
# TODO: add action button to notification


class TrelloColumn(ui.card):
    def __init__(self, bg_color: str) -> None:
        super().__init__(align_items=None)
        self.classes(f"min-w-32 h-fit min-h-24 bg-{bg_color}-200")


@router.page("/trello_cards")
def trello_example():
    next_list = ListBind(
        [
            {"label": "Simplify Layouting"},
            {"label": "Provide Deployment"},
        ]
    )
    doing_list = ListBind(
        [
            {"label": "Improve Documentation"},
        ]
    )
    done_list = ListBind(
        [
            {"label": "Invent NiceGUI"},
            {"label": "Test in own Projects"},
            {"label": "Publish as Open Source"},
            {"label": "Release Native-Mode"},
        ]
    )

    def on_drop(e):
        activity = e.args["old_list"].value[e.args["old_index"]]["label"]

        if e.args["new_list"] == sort1:
            ui.notify(f"Next up is `{activity}`", type="info")

        elif e.args["new_list"] == sort2:
            ui.notification(f"Doing `{activity}`", type="doing", spinner=True)

        elif e.args["new_list"] == sort3:
            ui.notify(f"`{activity}` is done!!", type="positive")

    def add_task():
        if new_task.value:
            sort1.insert(-1, {"label": new_task.value})
            # sort1.update() # Appending to list does not need `update()`
            new_task.value = ""

    with ui.row():
        with TrelloColumn("yellow"):
            ui.label("Next")
            sort1 = sortable.Column(
                value=next_list.value,
                class_obj=TrelloCard,
                group="trello",
                on_drop=on_drop,
            ).classes("w-full h-fit min-h-12 p-2 bg-yellow-100 rounded")

        with TrelloColumn("blue").classes("min-w-32 h-fit min-h-24"):
            ui.label("Doing")
            sort2 = sortable.Column(
                value=doing_list.value,
                class_obj=TrelloCard,
                group="trello",
                on_drop=on_drop,
            ).classes("w-full h-fit min-h-12 p-2 bg-blue-100 rounded")

        with TrelloColumn("red"):
            ui.label("Done")
            sort3 = sortable.Column(
                value=done_list.value,
                class_obj=TrelloCard,
                group="trello",
                on_drop=on_drop,
            ).classes("w-full h-fit min-h-12 p-2 bg-red-100 rounded")

    with ui.row(align_items="center"):
        new_task = ui.input("New Task").on("keyup.enter", add_task)
        ui.button(icon="add", on_click=add_task)
        ui.icon("o_info", size="sm", color="blue").tooltip(
            "You can delete with right click"
        )
