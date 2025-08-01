from typing import Any, Callable, Literal, Self

from nicegui.elements.mixins.value_element import ValueElement
from nicegui.events import GenericEventArguments


class Base(ValueElement, component="sortable.js", dependencies=["sortable.min.js"]):
    sortable_list: dict[int, Self] = {}

    def __init__(
        self,
        *,
        value: list[Any] | None = None,
        class_obj: type,
        group: str | None = None,
        on_drop: Callable | None = None,
    ) -> None:
        """Sortable Base Elemenmt

        Inspired by https://github.com/zauberzeug/nicegui/discussions/932 and
        https://github.com/itworkedlastime/nicegui-sortable-column

        This element futher improves by utilizing ValueElement rather generic Element.
        Thus, it can maintain the list of items (containing kwargs of `class_obj`) and
        automatically update the respective lists when the items are drag dropped.

        Using bindable list for value will automatically reflect the changes in value.
        Or you can still use the `.bind_value_to` function as well.

        Args:
            class_obj (type): type of class the children should be.
            value (list[Any], optional): list of keyword args for the `class_obj`. Defaults to None.
            group (str, optional): to group multiple drag drop containers. Defaults to None.
            on_drop (Callable, optional): callback function on `item-drop`. Defaults to None.
        """
        super().__init__(value=None, on_value_change=None, throttle=0)
        if value is not None:
            self.value: list[dict[str, Any]] = value
        else:
            self.value = []

        self.on("item-drop", self._handle_on_drop)
        self.on_drop: Callable | None = on_drop

        self.class_obj: type = class_obj
        self._props["group"] = group

        Base.sortable_list[self.id] = self

        with self:
            for val in self.value:
                self.class_obj(**val)

    def _handle_on_drop(self, e: GenericEventArguments) -> None:
        """Function to change index of the item dropped to respective lists.

        IMPORTANT: on_drop callback will pass args before change. So the value
        dropped will be at `e.args['old_list'].value[e.args['old_index']]`

        returns
            e.args
            - new_index: int
            - old_index: int
            - new_list: int => converted to Base class
            - old_list: int => converted to Base class

        Note:
            - `old_list` is the list that emits `item-drop` event and is `self` in this function.
            - `old_list` is not useful in this function but may useful `on_drop` callback.
            - `old_index` is useful this function but not so much in `on_drop` callback.
        """
        e.args["new_list"] = Base.sortable_list[e.args["new_list"]]
        e.args["old_list"] = Base.sortable_list[e.args["old_list"]]

        if self.on_drop is not None:
            self.on_drop(e)

        if self.id in (e.args["new_list"].id, e.args["old_list"].id):
            if e.args["new_list"].id == e.args["old_list"].id:
                self.internal_drop(e.args["old_index"], e.args["new_index"])
            else:
                self.external_drop(e.args)

    def internal_drop(self, old_index: int, new_index: int) -> None:
        """Called when the drop happenns in the same lists.

        Args:
            old_index (int): index the item was initially.
            new_index (int): index the item was dropped at.
        """

        if old_index != new_index:
            self.value.insert(new_index, self.value.pop(old_index))
            self.default_slot.children.insert(
                new_index, self.default_slot.children.pop(old_index)
            )

    def external_drop(self, args: dict[str, int | Self]) -> None:
        """Called when the drop happens in an another list.

        Args:
            args (dict[str, int  |  Self]): args emitted on `item-drop`.
            Contains index and `Base` class.
        """

        args["new_list"].value.insert(
            args["new_index"], self.value.pop(args["old_index"])
        )
        self.default_slot.children[args["old_index"]].move(
            args["new_list"], args["new_index"]
        )

    def pop(self, old_index: int) -> dict[str, Any]:
        """To remove an item manually.

        Useful to `delete` an item at index via a function.
        You must run `update()` after this to refresh contents.

        Args:
            old_index (int): index of the item to be popped.

        Returns:
            dict[str, Any]: returns the keyword args of the element.
        """

        self.remove(self.default_slot.children[old_index])
        return self.value.pop(old_index)

    def insert(self, new_index: int, obj: dict[str, Any]) -> None:
        """To insert an item manually.

        Useful to `insert` an item at index via a function.
        You must run `update()` after this to refresh contents.
        `update()` may not be needed if you append to the last.

        Args:
            new_index (int): index of the item to insert at.
            obj (dict[str, Any]): keyword args of the item.
        """
        if new_index < 0:
            self.value.append(obj)
        else:
            self.value.insert(new_index, obj)

        with self:
            self.class_obj(**obj)
        self.default_slot.children[-1].move(target_index=new_index)


class Row(Base, default_classes="nicegui-row"):
    def __init__(
        self,
        *,
        value: list[Any] | None = None,
        class_obj: type,
        group: str | None = None,
        wrap: bool = True,
        align_items: Literal["start", "end", "center", "baseline", "stretch"]
        | None = None,
        on_drop: Callable | None = None,
    ) -> None:
        """Sortable Row Element

        Derived from Sortable Base and ui.row

        Args:
            class_obj (type): type of class the childrens should be.
            value (list[Any], optional): list of keyword args for the `class_obj`. Defaults to None.
            group (str, optional): to group multiple drag drop containers. Defaults to None.
            wrap (bool, optional): whether to wrap the content. Defaults to False.
            align_items (Literal["start", "end", "center", "baseline", "stretch"], optional): alignment of the items in the column. Defaults to None.
            on_drop (Callable, optional): callback function on `item-drop`. Defaults to None.
        """
        super().__init__(
            value=value,
            class_obj=class_obj,
            group=group,
            on_drop=on_drop,
        )

        self._classes.append("row")

        if align_items:
            self._classes.append(f"items-{align_items}")

        if not wrap:
            self._style["flex-wrap"] = "nowrap"


class Column(Base, default_classes="nicegui-column"):
    def __init__(
        self,
        *,
        value: list[Any] | None = None,
        class_obj: type,
        group: str | None = None,
        wrap: bool = False,
        align_items: Literal["start", "end", "center", "baseline", "stretch"]
        | None = None,
        on_drop: Callable | None = None,
    ) -> None:
        """Sortable Column Element

        Derived from Sortable Base and ui.column

        Args:
            class_obj (type): type of class the childrens should be.
            value (list[Any], optional): list of keyword args for the `class_obj`. Defaults to None.
            group (str, optional): to group multiple drag drop containers. Defaults to None.
            wrap (bool, optional): whether to wrap the content. Defaults to False.
            align_items (Literal["start", "end", "center", "baseline", "stretch"], optional): alignment of the items in the column. Defaults to None.
            on_drop (Callable, optional): callback function on `item-drop`. Defaults to None.
        """
        super().__init__(
            value=value,
            class_obj=class_obj,
            group=group,
            on_drop=on_drop,
        )

        if align_items:
            self._classes.append(f"items-{align_items}")

        if wrap:
            self._style["flex-wrap"] = "wrap"
