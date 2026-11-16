# Terminal interface

Start `python Porn_Fetch_CLI.py` or `porn-fetch-cli` without arguments to open
Home. `--interactive` also opens the menus. All existing batch commands, flags,
settings JSON keys and configuration paths continue to work.

Home groups downloads, scraping, queues and saved jobs above administrative tools.
The compact header shows the version and current license status. Breadcrumbs show
the active feature. Returning from a tool restores the selected Home action;
settings categories and administrative menus also remember the selected item.

## Keyboard navigation

- Up/Down or Tab/Shift+Tab moves through menus, skipping unavailable actions.
- Enter activates the selected item; Escape returns from the current prompt.
- Page Up/Page Down moves through long menus. Ctrl+N/Ctrl+P also moves selection.
- In multi-selection lists, Space toggles a row and Enter confirms the selection.
- In settings, typing filters names, descriptions, values and original configuration
  keys. Backspace revises the filter; Ctrl+U clears it. A search with no matches
  cannot accidentally activate another setting.

Settings opens a category list, including Video, Library export, Performance,
Network, Cache, Logging and Database. Search all settings spans every category.
Each row shows a short name and value. The help area below the list describes the
highlighted setting and shows its original key and value. Edits use the existing
validation and save behavior. Reporting choices open the full consent disclosure;
consent bookkeeping fields are visible and managed by that flow. Proxy credentials
are hidden in lists.

## Small and limited terminals

Menus scroll within the available height and adapt when the terminal resizes.
At widths below 64 columns, multi-column tables become labeled records so values
remain readable. Download progress uses fewer columns on narrow terminals and
retains explicit byte, segment or item units. Long output remains in scrollback.

Set `PORNFETCH_PLAIN=1` for numbered, line-oriented menus without cursor control or
color. This mode is also selected automatically for `TERM=dumb` and non-TTY input
or output. Use a number to select a row, comma-separated numbers for multi-selection,
`/text` to filter a list, `/` to clear the filter, or `b` to return. Empty input keeps
the default text value; `/clear` supplies an empty value. EOF cancels a prompt.
`NO_COLOR` disables colors while preserving the visible selection pointer.

## Presentation architecture and checks

`src/cli/terminal.py` owns styling, sections, responsive tables, loading messages
and progress. `src/cli/prompts.py` provides a common prompt API: a small
prompt_toolkit selection layout with a separate scrolling list and contextual help,
Questionary text/password/confirmation/multi-selection prompts, and the plain
fallback. `src/cli/flows/ui.py` retains the former public presentation exports.
The feature flows continue to call the existing services for all application work.
No GUI framework or new dependency is required.

Run the focused offline checks with:

```sh
.venv/bin/python -m unittest src.tests.unit.test_cli_terminal src.tests.unit.test_cli_wizard src.tests.unit.test_cli_services src.tests.unit.test_cli_self_update
```

The terminal checks exercise 32x8, 40x12, 60x18, 80x24 and 120x40 layouts,
scrolling, contextual help, resize, Escape, filtering, disabled choices, plain
prompts, complete configuration-key coverage and the existing service workflows.
Provider and licensing servers are not contacted by these checks.
