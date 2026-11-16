"""One keyboard contract for interactive prompts, with a line-oriented fallback."""
from __future__ import annotations

import asyncio
import getpass
import os
import sys
from typing import Any

import questionary
from prompt_toolkit import Application
from prompt_toolkit.filters import to_filter
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Dimension, HSplit, Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.output import ColorDepth

from .terminal import WIZARD_STYLE, terminal_console

Choice = questionary.Choice
Separator = questionary.Separator


def plain_mode() -> bool:
    return os.environ.get("PORNFETCH_PLAIN", "").lower() in {"1", "true", "yes"} or (
        os.environ.get("TERM") == "dumb" or not sys.stdin.isatty() or not sys.stdout.isatty()
    )


class PlainPrompt:
    """Numbered menus never require cursor control, ANSI, or a Unicode font."""

    def __init__(self, kind: str, message: str, choices=(), **kwargs: Any):
        self.kind, self.message, self.choices, self.kwargs = kind, message, choices, kwargs

    async def ask_async(self):
        return await asyncio.to_thread(self.ask)

    def ask(self):
        console = terminal_console()
        console.print(self.message, markup=False)
        visible = list(self.choices)
        while True:
            options = []
            if self.kind in {"select", "checkbox"}:
                for item in visible:
                    if isinstance(item, Separator):
                        console.print(str(item.title), markup=False)
                        continue
                    choice = item if isinstance(item, Choice) else Choice(item)
                    options.append(choice)
                    label = choice.title if isinstance(choice.title, str) else "".join(t[1] for t in choice.title)
                    suffix = f" (unavailable: {choice.disabled})" if choice.disabled else ""
                    if choice.value == self.kwargs.get("default") and not choice.disabled:
                        suffix += " [default]"
                    if self.kind == "checkbox":
                        label = ("[x] " if choice.checked else "[ ] ") + label
                    console.print(f"  {len(options)}. {label}{suffix}", markup=False)
                    if choice.description:
                        console.print(f"     {choice.description}", markup=False)
                hint = "Numbers separated by commas" if self.kind == "checkbox" else "Number"
                prompt = f"{hint}, /text to filter, b to go back: "
            elif self.kind == "confirm":
                prompt = "[Y/n/b] " if self.kwargs.get("default", True) else "[y/N/b] "
            else:
                default = self.kwargs.get("default", "")
                prompt = f"[{default}] (/clear to empty) " if default and self.kind != "password" else "> "
            try:
                raw = getpass.getpass(prompt) if self.kind == "password" else input(prompt)
            except (EOFError, KeyboardInterrupt):
                return None
            if raw == "b" and self.kind in {"select", "checkbox", "confirm"}:
                return None
            if self.kind in {"select", "checkbox"}:
                if raw.startswith("/"):
                    query = raw[1:].casefold()
                    visible = [item for item in self.choices if not isinstance(item, Separator) and (
                        query in str(getattr(item, "title", item)).casefold()
                        or query in str(getattr(item, "description", "")).casefold()
                    )]
                    continue
                try:
                    if not raw.strip() and self.kind == "select":
                        default = self.kwargs.get("default")
                        selected = next((c for c in options if c.value == default and not c.disabled), None)
                        if selected:
                            return selected.value
                    if not raw.strip() and self.kind == "checkbox":
                        return [c.value for c in options if c.checked and not c.disabled]
                    indices = [int(value.strip()) for value in raw.split(",")]
                    if any(i < 1 or i > len(options) for i in indices):
                        raise ValueError
                    selected = [options[i - 1] for i in indices]
                    if not selected or any(c.disabled for c in selected):
                        raise ValueError
                    if self.kind == "select" and len(selected) != 1:
                        raise ValueError
                except (ValueError, IndexError):
                    console.print("Choose an available number from the list.", markup=False)
                    continue
                return selected[0].value if self.kind == "select" else list(dict.fromkeys(c.value for c in selected))
            if self.kind == "confirm":
                answer = raw.strip().lower()
                if not answer:
                    return self.kwargs.get("default", True)
                if answer in {"y", "yes", "n", "no"}:
                    return answer in {"y", "yes"}
                console.print("Enter y, n, or b.", markup=False)
                continue
            value = "" if raw == "/clear" else raw or self.kwargs.get("default", "")
            validator = self.kwargs.get("validate")
            if callable(validator):
                result = validator(value)
                if result is not True:
                    console.print(str(result or "Enter a valid value."), markup=False)
                    continue
            return value


def _prompt(kind: str, message: str, **kwargs):
    if plain_mode():
        return PlainPrompt(kind, message, **kwargs)
    kwargs.setdefault("style", WIZARD_STYLE)
    kwargs.setdefault("qmark", "")
    if "NO_COLOR" in os.environ:
        kwargs.setdefault("color_depth", ColorDepth.DEPTH_1_BIT)
    if kind in {"select", "checkbox"}:
        kwargs.setdefault("pointer", ">")
        kwargs.setdefault("instruction", "Arrows: move | Enter: select | Esc: back")
    prompt = getattr(questionary, kind)(message, **kwargs)
    # Questionary uses prompt_toolkit; bind Escape on this prompt only.
    navigation = KeyBindings()

    @navigation.add("escape", eager=True)
    def go_back(event):
        event.app.exit(result=None)

    prompt.application.key_bindings = merge_key_bindings([prompt.application.key_bindings, navigation])

    # Keep long lists scrollable on short terminals, leaving room for the prompt
    # and the current choice's contextual description. Recomputed on resize.
    if kind in {"select", "checkbox"}:
        for window in prompt.application.layout.find_all_windows():
            if isinstance(window, Window) and hasattr(window.content, "choices"):
                window.height = lambda: Dimension(max=max(2, prompt.application.output.get_size().rows - 8))
                window.wrap_lines = to_filter(False)
    return prompt


class Selection:
    """Selection state independent of terminal rendering and application services."""

    def __init__(self, choices, default=None):
        self.choices = [c if isinstance(c, Choice) else Choice(c) for c in choices]
        self.query = ""
        self.index = next((i for i, c in enumerate(self.choices) if c.value == default and self.enabled(c)), 0)
        if self.choices and not self.enabled(self.choices[self.index]):
            self.move(1)

    @staticmethod
    def enabled(choice):
        return not isinstance(choice, Separator) and not choice.disabled

    @property
    def visible(self):
        if not self.query:
            return self.choices
        return [c for c in self.choices if self.enabled(c) and self.query.casefold() in (
            f"{c.title} {c.description or ''}"
        ).casefold()]

    @property
    def current(self):
        return self.visible[self.index] if self.visible and self.index < len(self.visible) else None

    def filter(self, query):
        self.query = query
        self.index = 0

    def move(self, direction):
        options = self.visible
        if not options:
            return
        for _ in options:
            self.index = (self.index + direction) % len(options)
            if self.enabled(options[self.index]):
                return


def _select_prompt(message, choices, searchable=False, default=None, **kwargs):
    """Keep help separate from the scrolling list, including on short terminals."""
    state = Selection(choices, default)
    bindings = KeyBindings()

    def title():
        if app.output.get_size().columns < 64:
            hint = "Type / Arrows / Enter / Esc" if searchable else "Arrows Move / Enter OK / Esc Back"
        else:
            hint = ("Type: filter | " if searchable else "") + "Arrows/Tab: move | Enter: select | Esc: back"
        return [("class:question", message + "\n"), ("class:instruction", hint)]

    def rows():
        if not state.visible:
            return [("class:instruction", "No matches. Backspace to revise the filter.")]
        result = []
        for index, choice in enumerate(state.visible):
            current = index == state.index
            if current:
                result.append(("[SetCursorPosition]", ""))
            label = choice.title if isinstance(choice.title, str) else "".join(t[1] for t in choice.title)
            style = "class:separator" if isinstance(choice, Separator) else (
                "class:disabled" if choice.disabled else "class:highlighted" if current else "class:text"
            )
            suffix = f" ({choice.disabled})" if choice.disabled else ""
            result.append((style, ("> " if current else "  ") + label + suffix + "\n"))
        return result[:-1] + [(result[-1][0], result[-1][1].rstrip("\n"))]

    def details():
        choice = state.current
        description = (choice.description or str(choice.title)) if choice else ""
        position = f"{state.index + 1}/{len(state.visible)}" if choice else "0 matches"
        query = f"Filter: {state.query} | " if searchable else ""
        return [("class:instruction", f"{query}{position}\n{description}")]

    menu = Window(FormattedTextControl(rows, focusable=True), wrap_lines=False,
                  height=lambda: Dimension(min=1, max=max(1, app.output.get_size().rows - 8)))
    layout = Layout(HSplit([
        Window(FormattedTextControl(title), height=2, wrap_lines=False),
        menu,
        Window(FormattedTextControl(details), height=lambda: min(4, max(3, app.output.get_size().rows // 5)),
               wrap_lines=True),
    ]), focused_element=menu)

    @bindings.add("up")
    @bindings.add("s-tab")
    @bindings.add("c-p")
    def previous(event):
        state.move(-1)

    @bindings.add("down")
    @bindings.add("tab")
    @bindings.add("c-n")
    def following(event):
        state.move(1)

    @bindings.add("pageup")
    @bindings.add("pagedown")
    def page(event):
        direction = -1 if event.key_sequence[0].key == "pageup" else 1
        for _ in range(max(1, event.app.output.get_size().rows - 8)):
            state.move(direction)

    @bindings.add("escape", eager=True)
    @bindings.add("c-c")
    @bindings.add("c-q")
    def back(event):
        event.app.exit(result=None)

    @bindings.add("enter")
    def accept(event):
        if state.current and state.enabled(state.current):
            event.app.exit(result=state.current.value)

    @bindings.add("backspace")
    def erase(event):
        if searchable:
            state.filter(state.query[:-1])

    @bindings.add("c-u")
    def clear(event):
        state.filter("")

    @bindings.add("<any>")
    def type_query(event):
        if searchable and event.data.isprintable():
            state.filter(state.query + event.data)

    app = Application(layout=layout, key_bindings=bindings, style=kwargs.get("style", WIZARD_STYLE),
                      color_depth=ColorDepth.DEPTH_1_BIT if "NO_COLOR" in os.environ else None)
    return questionary.Question(app)


def select(message: str, choices, **kwargs):
    if plain_mode():
        return PlainPrompt("select", message, choices=choices, **kwargs)
    return _select_prompt(message, choices, **kwargs)


def checkbox(message: str, choices, **kwargs):
    kwargs.setdefault("instruction", "Arrows: move | Space: toggle | Enter: confirm | Esc: back")
    return _prompt("checkbox", message, choices=choices, **kwargs)


def text(message: str, **kwargs):
    return _prompt("text", message, **kwargs)


def password(message: str, **kwargs):
    return _prompt("password", message, **kwargs)


def confirm(message: str, **kwargs):
    return _prompt("confirm", message, **kwargs)
