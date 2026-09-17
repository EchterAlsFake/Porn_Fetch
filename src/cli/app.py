"""Textual full-screen terminal interface."""
from __future__ import annotations

import asyncio
from dataclasses import fields, replace
from datetime import datetime
from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Markdown, Static, Switch

from src.backend.media import VideoObject, select_allowed_quality
from src.backend.error_reporting import ERROR_REPORT_DISCLOSURE, ERROR_REPORT_EXAMPLE, report_exception
from .accounts import AccountService
from .downloads import DownloadOutcome, download_gallery, download_video
from .licensing import LicenseService, create_license_service
from .media import prepare_video
from .model_store import ModelStore
from .output import output_path_for
from .providers import ClientPool, ContentKind, Route, route_url, unwrap_scrape_result
from .settings import CliSettings, SettingsStore


SCREENS = (
    ("add", "Add Content"), ("results", "Results"), ("downloads", "Downloads"),
    ("tracked", "Tracked Models"), ("accounts", "Accounts"),
    ("settings", "Settings"), ("license", "License"), ("about", "About"),
)


class ErrorReportingConsentScreen(ModalScreen[bool]):
    """One-time, non-dismissible Textual consent choice."""

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="error-consent"):
            yield Label("Optional automatic error reports", classes="section-title")
            yield Static(ERROR_REPORT_DISCLOSURE)
            yield Label("Synthetic example of a stored report", classes="section-title")
            yield Static(ERROR_REPORT_EXAMPLE, id="error-consent-example")
            with Horizontal():
                yield Button("No, keep disabled", id="error-consent-no")
                yield Button("Yes, enable reports", id="error-consent-yes")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "error-consent-no":
            self.dismiss(False)
        elif event.button.id == "error-consent-yes":
            self.dismiss(True)


class Nav(Static):
    def compose(self) -> ComposeResult:
        with Horizontal(classes="nav"):
            for target, label in SCREENS:
                yield Button(label, id=f"nav-{target}", variant="primary" if target == "add" else "default")


class BaseScreen(Screen):
    def compose_header(self):
        yield Header()
        yield Nav()

    def compose_footer(self):
        yield Footer()


class AddScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        with Vertical(id="add-content"):
            yield Label("Video, profile, playlist, collection, or XFreeHD album URL")
            yield Input(placeholder="https://…", id="url-input")
            yield Button("Load", id="submit-url", variant="success")
            yield Static("", id="add-status")
        yield from self.compose_footer()


class ResultsScreen(BaseScreen):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[tuple[Route, Any, VideoObject | None]] = []
        self.selected: set[int] = set()

    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        yield DataTable(id="results-table", cursor_type="row", zebra_stripes=True)
        with Horizontal():
            yield Input(placeholder="Quality (best, 720, …)", id="result-quality")
            yield Button("Toggle selected", id="toggle-result")
            yield Button("Queue selected", id="queue-selected", variant="success")
        yield from self.compose_footer()

    def on_mount(self) -> None:
        self._ensure_columns()
        self._render_items()

    def _ensure_columns(self) -> None:
        table = self.query_one("#results-table", DataTable)
        if table.columns:
            return
        for label, key in (("", "selected"), ("Title", "title"), ("Author", "author"), ("Duration", "duration"), ("Qualities", "qualities")):
            table.add_column(label, key=key)

    def replace_items(self, items: list[tuple[Route, Any, VideoObject | None]]) -> None:
        self.items = items
        self.selected.clear()
        if self.is_mounted:
            self._render_items()

    def _render_items(self) -> None:
        self._ensure_columns()
        table = self.query_one("#results-table", DataTable)
        table.clear()
        for index, (route, source, media) in enumerate(self.items):
            if media is None:
                table.add_row(" ", getattr(source, "title", "Album"), route.provider, "—", "images", key=str(index))
            else:
                duration = "—" if media.length is None else f"{media.length} min"
                table.add_row(" ", media.title, media.author, duration, ", ".join(f"{q}p" for q in media.qualities), key=str(index))

    def current_index(self) -> int | None:
        table = self.query_one("#results-table", DataTable)
        if not self.items or table.cursor_row < 0:
            return None
        return table.cursor_row

    def toggle(self) -> None:
        index = self.current_index()
        if index is None:
            return
        if index in self.selected:
            self.selected.remove(index)
            marker = " "
        else:
            self.selected.add(index)
            marker = "✓"
        self.query_one("#results-table", DataTable).update_cell(str(index), "selected", marker)


class DownloadsScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        yield Static("0 / 0 jobs complete", id="overall-progress")
        yield DataTable(id="downloads-table", cursor_type="row", zebra_stripes=True)
        with Horizontal():
            yield Button("Cancel", id="cancel-download", variant="warning")
            yield Button("Retry", id="retry-download")
        yield from self.compose_footer()

    def on_mount(self) -> None:
        self.ensure_columns()

    def ensure_columns(self) -> None:
        table = self.query_one("#downloads-table", DataTable)
        if table.columns:
            return
        for label, key in (("Title", "title"), ("Quality", "quality"), ("Progress", "progress"), ("Status", "status")):
            table.add_column(label, key=key)


class TrackedScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        with Horizontal():
            yield Input(placeholder="Profile URL", id="tracked-url")
            yield Button("Add", id="tracked-add")
            yield Button("Remove", id="tracked-remove", variant="warning")
            yield Button("Scan", id="tracked-scan")
            yield Button("Download pending", id="tracked-download", variant="success")
        yield DataTable(id="tracked-table", cursor_type="row", zebra_stripes=True)
        yield from self.compose_footer()

    def on_mount(self) -> None:
        table = self.query_one("#tracked-table", DataTable)
        for label, key in (("Profile", "profile"), ("Downloaded", "downloaded"), ("Pending", "pending")):
            table.add_column(label, key=key)
        self.refresh_rows()

    def refresh_rows(self) -> None:
        table = self.query_one("#tracked-table", DataTable)
        table.clear()
        for url, state in self.app.model_store.models():
            table.add_row(url, len(state["downloaded"]), len(state["pending"]), key=url)


class AccountsScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        with Vertical(id="account-form"):
            yield Label("Provider: PornHub, XHamster, or XVideos")
            yield Input(value="PornHub", id="account-provider")
            yield Input(placeholder="Email / username / session_token", password=True, id="account-user")
            yield Input(placeholder="Password / session_token_auth", password=True, id="account-secret")
            with Horizontal():
                yield Button("Login", id="account-login", variant="success")
                yield Button("Use browser cookies", id="account-browser")
            yield Input(placeholder="Collection: history, favorites, liked, recommended, watch_later, playlist", id="account-collection")
            yield Input(placeholder="Authenticated XHamster playlist URL (if needed)", id="account-playlist")
            yield Button("Load account collection", id="account-load")
            yield Static("Credentials and tokens are kept in memory only.", id="account-status")
        yield from self.compose_footer()


SETTING_GROUPS = {
    "Video": list(range(0, 9)),
    "Performance": list(range(9, 25)),
    "Network / Privacy": list(range(25, 38)),
    "Logging": list(range(38, 41)),
    "Appearance": [42],
}


class SettingsScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        all_fields = list(fields(CliSettings))
        with VerticalScroll(id="settings-form"):
            for group, indexes in SETTING_GROUPS.items():
                yield Label(group, classes="section-title")
                for index in indexes:
                    field = all_fields[index]
                    value = getattr(self.app.settings, field.name)
                    yield Label(field.name.replace("_", " ").title())
                    if isinstance(value, bool):
                        yield Switch(value=value, id=f"setting-{field.name}")
                    else:
                        yield Input(value=str(value), id=f"setting-{field.name}")
            yield Button("Save settings", id="save-settings", variant="success")
            yield Static("", id="settings-status")
        yield from self.compose_footer()

    def save(self) -> None:
        values: dict[str, Any] = {}
        for field in fields(CliSettings):
            if field.name == "error_reporting_decided":
                values[field.name] = True
                continue
            current = getattr(self.app.settings, field.name)
            widget = self.query_one(f"#setting-{field.name}")
            if isinstance(widget, Switch):
                values[field.name] = widget.value
            else:
                raw = widget.value
                values[field.name] = type(current)(raw) if not isinstance(current, str) else raw
        updated = CliSettings(**values)
        updated.validate()
        self.app.settings_store.save(updated)
        self.app.settings = updated
        try:
            self.app.theme = updated.theme
        except Exception:
            pass
        self.query_one("#settings-status", Static).update(
            "Saved. Network clients and in-memory accounts will refresh when downloads are idle."
        )
        self.app.request_pool_rebuild()


class LicenseScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        with Vertical():
            yield Static("Checking license…", id="license-status")
            yield Input(placeholder="Path to schema-2 license file", id="license-path")
            with Horizontal():
                yield Button("Import", id="license-import")
                yield Button("Refresh", id="license-refresh")
                yield Button("Deactivate", id="license-deactivate", variant="warning")
        yield from self.compose_footer()

    def on_mount(self) -> None:
        self.call_after_refresh(self.app._show_license)


class AboutScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from self.compose_header()
        credits = Path(__file__).resolve().parents[2] / "README" / "CREDITS.md"
        yield Markdown(credits.read_text(encoding="utf-8"), id="about-credits")
        yield from self.compose_footer()


class PornFetchApp(App):
    TITLE = "Porn Fetch"
    CSS = """
    ErrorReportingConsentScreen { align: center middle; }
    .nav { height: 3; overflow-x: auto; }
    .nav Button { min-width: 14; margin-right: 1; }
    #add-content, #account-form { padding: 2 4; }
    #results-table, #downloads-table, #tracked-table { height: 1fr; }
    #settings-form { padding: 1 4; }
    .section-title { margin-top: 1; text-style: bold; color: $accent; }
    Input { margin-bottom: 1; }
    #error-consent { width: 90%; height: 90%; padding: 1 2; background: $surface; border: round $accent; }
    #error-consent-example { padding: 1; background: $panel; }
    """
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self) -> None:
        self.settings_store = SettingsStore()
        self.settings = self.settings_store.load()
        self.model_store = ModelStore()
        self.pool: ClientPool | None = None
        self.licenses: LicenseService | None = None
        self.accounts: AccountService | None = None
        self.jobs: list[dict[str, Any]] = []
        self.job_tasks: dict[int, asyncio.Task[Any]] = {}
        self._pool_rebuild_pending = False
        self.download_semaphore: asyncio.Semaphore | None = None
        self._tracking_origin: str | None = None
        super().__init__()

    def on_mount(self) -> None:
        try:
            self.theme = self.settings.theme
        except Exception:
            pass
        self.pool = ClientPool(self.settings.to_runtime_config())
        self.licenses = create_license_service(self.settings.to_runtime_config())
        self.accounts = AccountService(self.pool)
        self.download_semaphore = asyncio.Semaphore(max(1, self.settings.parallel_downloads))
        self.install_screen(AddScreen(), "add")
        self.install_screen(ResultsScreen(), "results")
        self.install_screen(DownloadsScreen(), "downloads")
        self.install_screen(TrackedScreen(), "tracked")
        self.install_screen(AccountsScreen(), "accounts")
        self.install_screen(SettingsScreen(), "settings")
        self.install_screen(LicenseScreen(), "license")
        self.install_screen(AboutScreen(), "about")
        self.push_screen("add")
        if not self.settings.error_reporting_decided:
            self.push_screen(ErrorReportingConsentScreen(), self._save_error_reporting_consent)
        self.run_worker(self._check_license(), group="license", exclusive=True)

    def _save_error_reporting_consent(self, enabled: bool | None) -> None:
        if enabled is None:
            return
        self.settings = replace(
            self.settings,
            error_reporting=enabled,
            error_reporting_decided=True,
        )
        self.settings_store.save(self.settings)

    async def on_unmount(self) -> None:
        if self.licenses:
            await self.licenses.close()
        if self.pool:
            await self.pool.close()

    async def _report(
        self, error: BaseException, operation: str, location: str, **context: Any,
    ) -> str:
        return await report_exception(
            error,
            operation=operation,
            location=location,
            context=context,
            enabled=self.settings.error_reporting,
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button.id or ""
        if button.startswith("nav-"):
            target = button.removeprefix("nav-")
            self.switch_screen(target)
            if target == "license":
                self.call_after_refresh(self._show_license)
        elif button == "submit-url":
            url = self.get_screen("add").query_one("#url-input", Input).value
            self.run_worker(self._load_url(url), group="load", exclusive=True)
        elif button == "toggle-result":
            self.get_screen("results").toggle()
        elif button == "queue-selected":
            await self._queue_selected()
        elif button == "cancel-download":
            self._cancel_current()
        elif button == "retry-download":
            self._retry_current()
        elif button == "save-settings":
            try:
                self.get_screen("settings").save()
            except ValueError as error:
                self.get_screen("settings").query_one("#settings-status", Static).update(str(error))
        elif button.startswith("tracked-"):
            await self._tracked_action(button.removeprefix("tracked-"))
        elif button.startswith("account-"):
            if button == "account-load":
                self.run_worker(self._account_collection(), group="account", exclusive=True)
            else:
                self.run_worker(self._account_login(button == "account-browser"), group="account", exclusive=True)
        elif button.startswith("license-"):
            self.run_worker(self._license_action(button.removeprefix("license-")), group="license", exclusive=True)

    async def _load_url(self, url: str) -> None:
        status = self.get_screen("add").query_one("#add-status", Static)
        status.update("Loading…")
        try:
            route = route_url(url)
            items: list[tuple[Route, Any, VideoObject | None]] = []
            async for source in self.pool.media_stream(url, pages=5):
                media = None if route.kind == ContentKind.GALLERY else await prepare_video(source, route.provider)
                items.append((route, source, media))
                if len(items) >= self.settings.result_limit:
                    break
            self.switch_screen("results")
            await asyncio.sleep(0)
            self.get_screen("results").replace_items(items)
            status.update(f"Loaded {len(items)} item(s) from {route.provider}.")
        except Exception as error:
            report_id = await self._report(
                error, "load media URL", "src.cli.app.PornFetchApp._load_url",
                source_url=url,
            )
            status.update(f"Could not load URL: {error} [error {report_id}]")

    async def _queue_selected(self) -> None:
        screen: ResultsScreen = self.get_screen("results")
        indexes = sorted(screen.selected) or ([screen.current_index()] if screen.current_index() is not None else [])
        requested = screen.query_one("#result-quality", Input).value.strip() or self.settings.quality
        pending_jobs = []
        for index in indexes:
            route, source, media = screen.items[index]
            quality = requested if media is None else select_allowed_quality(requested, media.qualities, self.licenses.status.allowed)
            if media is not None and not quality:
                quality = select_allowed_quality("720", media.qualities, False)
            job = {"route": route, "source": source, "media": media, "quality": quality, "status": "queued", "progress": None, "event": asyncio.Event(), "tracking_origin": self._tracking_origin}
            self.jobs.append(job)
            row = len(self.jobs) - 1
            pending_jobs.append((row, job))
        self.switch_screen("downloads")
        await asyncio.sleep(0)
        table = self.get_screen("downloads").query_one("#downloads-table", DataTable)
        self.get_screen("downloads").ensure_columns()
        for row, job in pending_jobs:
            media = job["media"]
            source = job["source"]
            title = getattr(media, "title", None) or getattr(source, "title", "Album")
            table.add_row(title, job["quality"] or "images", "…", "queued", key=str(row))
            worker = self.run_worker(self._run_job(row), group="downloads")
            self.job_tasks[row] = worker
        self._update_overall()

    async def _run_job(self, index: int) -> None:
        job = self.jobs[index]
        job["status"] = "downloading"
        self._update_job(index)
        try:
            async with self.download_semaphore:
                if self.settings.processing_delay:
                    await asyncio.sleep(self.settings.processing_delay)
                media = job["media"]
                if media is None:
                    outcome = await download_gallery(job["source"], self.settings.output_path, stop_event=job["event"], progress=lambda value: self._progress(index, value), concurrency=self.settings.videos_concurrency)
                else:
                    job["quality"] = select_allowed_quality(
                        job["quality"], media.qualities, self.licenses.status.allowed,
                    )
                    if not job["quality"]:
                        raise ValueError("No permitted quality is available")
                    self._update_job(index)
                    target = output_path_for(media, self.settings)
                    outcome = await download_video(job["source"], target, job["quality"], self.settings, has_premium=self.licenses.status.allowed, stop_event=job["event"], progress=lambda value: self._progress(index, value), available_qualities=media.qualities)
                job["outcome"] = outcome
                job["status"] = outcome.status
                if outcome.status not in {"completed", "cancelled"}:
                    job["error_id"] = await self._report(
                        RuntimeError(f"Downloader returned status {outcome.status}"),
                        "download queued media",
                        "src.cli.app.PornFetchApp._run_job",
                        video_url=getattr(media, "url", None) or getattr(job["source"], "url", None),
                        provider=getattr(job.get("route"), "provider", None),
                        quality=job.get("quality"),
                    )
                if (
                    media is not None and outcome.status == "completed"
                    and not outcome.skipped and outcome.path.suffix.casefold() == ".mp4"
                    and outcome.path.exists() and self.settings.write_metadata
                ):
                    try:
                        from src.backend.metadata import write_tags
                        write_tags(str(outcome.path), media)
                    except Exception as error:
                        job["metadata_warning"] = str(error)
                        await self._report(
                            error, "write downloaded video metadata",
                            "src.cli.app.PornFetchApp._run_job",
                            video_url=getattr(media, "url", None),
                            provider=getattr(job.get("route"), "provider", None),
                        )
                if outcome.status == "completed" and job["tracking_origin"] and media is not None:
                    self.model_store.mark_downloaded(job["tracking_origin"], media.url)
        except asyncio.CancelledError:
            job["status"] = "cancelled"
            raise
        except Exception as error:
            job["status"] = "failed"
            job["error"] = str(error)
            source = job.get("source")
            media = job.get("media")
            job["error_id"] = await self._report(
                error, "download queued media", "src.cli.app.PornFetchApp._run_job",
                video_url=getattr(media, "url", None) or getattr(source, "url", None),
                provider=getattr(job.get("route"), "provider", None),
                quality=job.get("quality"),
            )
        finally:
            self._update_job(index)
            self._update_overall()
        if self._pool_rebuild_pending and not any(item["status"] == "downloading" for item in self.jobs):
            await self._rebuild_pool()

    def _progress(self, index: int, value: int | None) -> None:
        self.jobs[index]["progress"] = value
        self._update_job(index)

    def _update_job(self, index: int) -> None:
        job = self.jobs[index]
        table = self.get_screen("downloads").query_one("#downloads-table", DataTable)
        shown = "…" if job["progress"] is None else f"{job['progress']}%"
        table.update_cell(str(index), "quality", job["quality"] or "images")
        table.update_cell(str(index), "progress", shown)
        table.update_cell(str(index), "status", job["status"])

    def _update_overall(self) -> None:
        done = sum(job["status"] in {"completed", "failed", "cancelled"} for job in self.jobs)
        self.get_screen("downloads").query_one("#overall-progress", Static).update(f"{done} / {len(self.jobs)} jobs complete")

    def _current_job(self) -> int | None:
        table = self.get_screen("downloads").query_one("#downloads-table", DataTable)
        return table.cursor_row if self.jobs and table.cursor_row >= 0 else None

    def _cancel_current(self) -> None:
        index = self._current_job()
        if index is not None:
            self.jobs[index]["event"].set()

    def _retry_current(self) -> None:
        index = self._current_job()
        if index is not None and self.jobs[index]["status"] in {"failed", "cancelled"}:
            self.jobs[index]["event"] = asyncio.Event()
            self.jobs[index]["status"] = "queued"
            self.job_tasks[index] = self.run_worker(self._run_job(index), group="downloads")

    async def _tracked_action(self, action: str) -> None:
        screen: TrackedScreen = self.get_screen("tracked")
        url = screen.query_one("#tracked-url", Input).value.strip()
        if action == "add":
            self.model_store.add(url)
        elif action == "remove":
            self.model_store.remove(url)
        elif action == "scan":
            targets = [url] if url else [item[0] for item in self.model_store.models()]
            for target in targets:
                found = []
                async for video in self.pool.media_stream(target, pages=5):
                    if getattr(video, "url", None):
                        found.append(video.url)
                self.model_store.update_pending(target, found)
        elif action == "download":
            for model, state in self.model_store.models():
                for pending in state["pending"]:
                    await self._load_url(pending)
                    results: ResultsScreen = self.get_screen("results")
                    results.selected = {0}
                    self._tracking_origin = model
                    await self._queue_selected()
                    self._tracking_origin = None
        screen.refresh_rows()

    async def _account_login(self, browser: bool) -> None:
        screen = self.get_screen("accounts")
        provider = screen.query_one("#account-provider", Input).value
        user = screen.query_one("#account-user", Input).value
        secret = screen.query_one("#account-secret", Input).value
        try:
            tokens = {"session_token": user, "session_token_auth": secret} if provider.casefold() == "xvideos" else None
            ok = await self.accounts.login(provider, username=user, password=secret, tokens=tokens, browser=browser)
            screen.query_one("#account-status", Static).update("Logged in." if ok else "Login failed.")
        except Exception as error:
            await self._report(
                error, "authenticate account", "src.cli.app.PornFetchApp._account_login",
                provider=provider,
            )
            screen.query_one("#account-status", Static).update(str(error))

    async def _account_collection(self) -> None:
        screen = self.get_screen("accounts")
        provider = screen.query_one("#account-provider", Input).value.casefold()
        collection = screen.query_one("#account-collection", Input).value
        playlist = screen.query_one("#account-playlist", Input).value
        try:
            stream, _ = self.accounts.collection(provider, collection, playlist)
            route = Route(provider, ContentKind.COLLECTION, playlist or f"https://{provider}.com/account")
            items = []
            try:
                async for result in stream:
                    source = unwrap_scrape_result(result)
                    items.append((route, source, await prepare_video(source, provider)))
                    if len(items) >= self.settings.result_limit:
                        break
            finally:
                close = getattr(stream, "aclose", None)
                if close:
                    await close()
            self.switch_screen("results")
            await asyncio.sleep(0)
            self.get_screen("results").replace_items(items)
        except Exception as error:
            await self._report(
                error, "fetch account collection", "src.cli.app.PornFetchApp._account_collection",
                provider=provider, collection=collection, playlist_url=playlist,
            )
            screen.query_one("#account-status", Static).update(str(error))

    async def _check_license(self) -> None:
        try:
            await self.licenses.check()
        except Exception:
            pass
        self._show_license()

    async def _license_action(self, action: str) -> None:
        try:
            if action == "import":
                path = self.get_screen("license").query_one("#license-path", Input).value
                await self.licenses.import_file(path)
            elif action == "refresh":
                await self.licenses.check(force=True)
            elif action == "deactivate":
                await self.licenses.deactivate()
        except Exception as error:
            await self._report(
                error, "manage license", "src.cli.app.PornFetchApp._license_action",
                action=action,
            )
            self.get_screen("license").query_one("#license-status", Static).update(str(error))
            return
        self._show_license()

    def _show_license(self) -> None:
        status = self.licenses.status
        expiry = "—" if status.expires_at is None else datetime.fromtimestamp(status.expires_at).astimezone().isoformat(timespec="minutes")
        screen = self.get_screen("license")
        if screen.is_mounted:
            screen.query_one("#license-status", Static).update(f"State: {status.state}\n{self.licenses.reason}\nExpiry: {expiry}")

    def request_pool_rebuild(self) -> None:
        if any(job["status"] in {"queued", "downloading"} for job in self.jobs):
            self._pool_rebuild_pending = True
        else:
            self.run_worker(self._rebuild_pool(), group="pool", exclusive=True)

    async def _rebuild_pool(self) -> None:
        old = self.pool
        old_licenses = self.licenses
        self.pool = ClientPool(self.settings.to_runtime_config())
        self.licenses = create_license_service(self.settings.to_runtime_config())
        try:
            await self.licenses.check()
        except Exception:
            pass
        self.accounts = AccountService(self.pool)
        self.download_semaphore = asyncio.Semaphore(max(1, self.settings.parallel_downloads))
        self._pool_rebuild_pending = False
        await old_licenses.close()
        await old.close()
        self._show_license()
