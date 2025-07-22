# nicegui-custom-elements

Some nicegui custom elements to make ui.page clutter free (to some extent).

Elements featured in this repo are meant to modified. For example, `TabbedHeader` does not feature any action buttons.
Either they need to added inside the function or you would need to modify the class to include those via a parameter.

Though for a generic case, most of the elements should be okay as is, you are free to modify them as you see fit.

## Usage

Dont import the class as is, import the file and access the classes via it.

For example, `List`, `Item` and `MiniDrawer` in `nav_rail.py` are to be accessed like `nav_rail.List`, `nav_rail.Item` and `nav_rail.MiniDrawer`
so that the class names do not overlap (similar to how everything is `ui.~` in nicegui).

## License

This repo is licensed under MIT.