## Some useful JS/CSS Scripts

JS_SCRIPT_PREVENT_RELOAD = """
<script>
  window.addEventListener('beforeunload', function (e) {
    if (document.querySelector('.do-not-reload')) {
      e.preventDefault();
    }
  });
</script>
"""

JS_SCRIPT_DETECT_THEME = """
    if (Quasar.Dark.mode == "auto")
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    else
        return Quasar.Dark.mode;
"""

CSS_HIDE_SCROLLBAR = """
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
"""

# Use `scrollbar-hide` class along with `overflow-x-auto flex-nowrap w-full`
# and optionally with `gap-1` to have close packing
# USE THIS WITH CAUTION, though it does not break anything, this will remove
# the only indicaton that there is a section that can be scrolled.

CSS_MINIMAL_SCROLLBAR = """
.chip-box::-webkit-scrollbar {
  height: 8px;
}

.chip-box::-webkit-scrollbar-thumb {
  background: #5898d4;
  border-radius: 4px;
}

.chip-box::-webkit-scrollbar-track {
  background: #f1f1f1;
}
"""

# Use `chip-box` class along with `overflow-x-auto flex-nowrap w-full`
# and optionally with `gap-1` to have close packing
# This is used when you want to have a slimmer scrollbar than default.


JS_AUTO_TOGGLE_CLASSES = """
const target = document.querySelector('.nicegui-aggrid');

function updateThemeClass(e) {
  if (!target) return;
  target.classList.remove('ag-theme-material', 'ag-theme-material-dark');
  target.classList.add(e ? 'ag-theme-material-dark' : 'ag-theme-material');
}

function isDarkTheme() {
  if (Quasar.Dark.mode == "auto")
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  else
    return Quasar.Dark.mode
}

updateThemeClass(isDarkTheme());
"""

# This JS needs to bundled with ui.dark_mode on value change function.
