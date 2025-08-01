# nicegui-custom-elements

Some nicegui custom elements to make ui.page clutter free (to some extent).

Elements featured in this repo are meant to modified. For example, `TabbedHeader` does not feature any action buttons.
Either they need to added inside the function or you would need to modify the class to include those via a parameter.

Though for a generic case, most of the elements should be okay as is, you are free to modify them as you see fit.

## Usage

Dont import the class as is, import the file and access the classes via it.

For example, `List`, `Item` and `MiniDrawer` in `nav_rail.py` are to be accessed like `nav_rail.List`, `nav_rail.Item` and `nav_rail.MiniDrawer`
so that the class names do not overlap (similar to how everything is `ui.~` in nicegui).

## Examples

I decided to change the repo from being just a collection of elements to a nicegui app to run. So it is possible to run and see the examples in action (at least once).

Currently only sortable example is added and others would follow if I get the time.

### Features

#### Sortable

- This element requires 2 or 3 files: `sortable.js`, `sortable.py` and `sortable.min.js` (optional). `sortable.min.js` can be removed if `sortable.js` imports it via URL like `https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.6/Sortable.min.js` either way you need to change the version if you ever need to update it. Ultimately, I did not want to call `cdnjs.cloudflare.com` for the JS file. Also `sortable.min.js` (in dependencies in Base class) == `sortable` (import in `sortable.js`).
- `sortable.Row`, `sortable.Column` and `sortable.Grid` uses [SortableJS](https://github.com/SortableJS/Sortable) to drag and rearrange the elements in list/s.
- Only sortables in same `group` allows elements to drag drop interchangeably.
- You can also use functions to add/remove elements to the list.
- It is a value element, so you can bind value to a variable or you can use a list bind as a value as well. Each element of the value must be the kwargs of the `class_obj` parameter.
- Some limitations:
    - can have only one `class_obj` per sortable container. It is possible to have drag and drop between 2 class_obj/container but it required to refresh the element (which started causing pop index out of range errors though it reality not). Also you need to have `**kwargs` in both classes if the parameters are not same.
    - can not toggle sortable on and off. Not sure how to.
    - can not use nested sortables (did not explorer it and prolly will not for now).
    - can not drag multiple (did not explorer it and never prolly will).


## License

This repo is licensed under MIT.
