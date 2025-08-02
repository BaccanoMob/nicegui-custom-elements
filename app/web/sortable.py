import random

from nicegui import APIRouter, ui

from app.custom import sortable
from app.custom.binds import ListBind

router = APIRouter(prefix="/sortable")


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


@router.page("/")
def sortable_example():
    ui.button("elements").on_click(lambda: ui.navigate.to(sortable_elements))
    ui.button("updates").on_click(lambda: ui.navigate.to(sortable_updates))
    ui.button("groups").on_click(lambda: ui.navigate.to(sortable_group))
    ui.button("dropzone").on_click(lambda: ui.navigate.to(sortable_dropzone))
    ui.button("all").on_click(lambda: ui.navigate.to(sortable_all))
    ui.button("trello_cards").on_click(lambda: ui.navigate.to(trello_example))


@router.page("/all")
def sortable_all():
    draw()


@router.page("/elements")
def sortable_elements():
    list1 = ListBind([{"label": str(i)} for i in range(20, 24)])
    list2 = ListBind([{"label": str(i)} for i in range(30, 36)])
    list3 = ListBind([{"label": str(i)} for i in range(0, 15)])

    with ui.row():
        with ui.card():
            ui.label("Row").classes("text-center w-full")
            sortable.Row(value=list1.value, class_obj=Custom, group="a")

        with ui.card():
            ui.label("Column").classes("text-center w-full")
            sortable.Column(value=list2.value, class_obj=Custom, group="a")

        with ui.card():
            ui.label("Grid").classes("text-center w-full")
            sortable.Grid(value=list3.value, class_obj=Custom, group="a", columns=4)


@router.page("/updates")
def sortable_updates():
    def pop():
        try:
            sort1.pop(0)
            sort1.update()
        except Exception as e:
            ui.notify(str(e))

    def insert():
        sort1.insert(0, {"label": f"{random.randint(0, 100)}"})
        sort1.update()

    list1 = ListBind([{"label": str(i)} for i in range(3)])

    with ui.card():
        ui.label("sort1")
        sort1 = sortable.Row(value=list1.value, class_obj=Custom, group="a")

    with ui.row():
        ui.button("pop", on_click=pop).tooltip("Pop first element of list")
        ui.button("insert", on_click=insert).tooltip(
            "Add a random number to start of list"
        )


@router.page("/groups")
def sortable_group():
    list1 = ListBind([{"label": str(i)} for i in range(3)])
    list2 = ListBind([{"label": str(i)} for i in range(20, 24)])
    with ui.card():
        ui.label("sort1")
        sortable.Row(value=list1.value, class_obj=Custom, group="a")

    with ui.card():
        ui.label("sort1")
        sortable.Row(value=list2.value, class_obj=Custom, group="a")


@router.page("/dropzone")
def sortable_dropzone():
    list1 = ListBind([{"label": str(i)} for i in range(10)])
    list2 = ListBind()
    with ui.card():
        sortable.Row(value=list1.value, class_obj=Custom, group="a")

    with ui.card().classes("min-w-32 h-fit min-h-24 bg-blue-200"):
        ui.label("Drop Here")
        sortable.Row(
            value=list2.value,
            class_obj=Custom,
            group="a",
        ).classes("w-full h-fit min-h-12 p-2 bg-blue-100 rounded")

    with ui.card().classes("min-w-32 h-fit min-h-24 bg-blue-200"):
        ui.label("Drop here?")
        sortable.Row(
            value=list2.value,
            class_obj=Custom,
            group="a",
        ).classes("border-[2px]")
    with ui.label("Good luck dropping above!"):
        ui.label(
            "It's possible but without elements the size of container is really small"
        )
        ui.label("Try the left most spot (marked with a border)")


class TrelloCard(ui.card):
    def __init__(self, *, label: str) -> None:
        super().__init__(align_items=None)
        self.label: str = label
        with self.classes("w-full"):
            ui.label(label)
            with ui.context_menu():
                ui.menu_item("Edit", on_click=self._edit_card, auto_close=False)
                # auto close should be false for dialog to show
                ui.separator()
                ui.menu_item("Delete", on_click=self._delete_card)

    def _edit_card(self):
        def _update_label():
            dialog.close()
            parent: sortable.Base = self.parent_slot.parent
            index = parent.default_slot.children.index(self)
            data = parent.pop(index)
            data.update({"label": label.value})
            parent.insert(index, data)

        with ui.dialog() as dialog:
            with ui.card():
                label = ui.input("Label", value=self.label).props("autofocus")
                label.on("keyup.enter", _update_label)
        dialog.open()
        # data = parent.pop(index)

    def _delete_card(self):
        def undo():
            parent.insert(index, data)
            parent.update()

        parent: sortable.Base = self.parent_slot.parent
        index = parent.default_slot.children.index(self)
        data = parent.pop(index)
        # ui.notify(f"{data['label']} deleted!!", type="warning")
        n = ui.notification(
            f"{data['label']} deleted!!",
            type="warning",
            # actions=[
            #     {
            #         "label": "Undo",
            #         ":handler": '() => {emitEvent("undo")}',
            #     }
            # ],
        )

        # ui.on("undo", undo)

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
