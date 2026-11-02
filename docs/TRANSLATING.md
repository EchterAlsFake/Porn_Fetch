# Translate Porn Fetch

Translations use Qt TS files, edited in a browser with self-hosted Weblate.
Qt Linguist and programming experience are not required. The translation service
has not been deployed yet; the maintainer will add its public link here after setup.
Until then, translation file contributions can be submitted through GitHub.

1. Install the GUI to understand the screen you are translating.
2. Open **Info → Help translate**, follow the service link, and create an account.
3. Select your language and translate or suggest improvements. Read the context,
   developer notes and screenshots. Leave product names, URLs and placeholders
   such as `%1`, `%n`, `$title` and `${title}` intact. Translate whole sentences;
   their word order may differ from English. Fill every plural form.
4. Ask a reviewer to approve your work. Report confusing English text rather than
   guessing. Contributions are included under the repository's application license;
   only submit text you have permission to contribute.
5. A maintainer opens a translation PR and runs **Translation validation and
   previews** on that branch. Download its artifact for your desktop OS, extract
   the whole folder, then run the executable. Windows development previews use
   the `signing` environment and Certum signing; other previews remain unsigned.
   Android previews use **Build All** on the reviewed branch with Android selected
   and publication switches disabled; signing stays in that existing trusted workflow.
6. Select your language in Settings and check wrapping, dialogs and screen-reader
   descriptions. Approved changes ship in the next release.

English remains visible when a translation is missing. No translation-site account
or network connection is needed to use the app. Language preferences are separate
from the language of provider content.

## Maintainer workflow

Run `uv run python scripts/translations.py extract` after GUI text changes and
commit the updated TS catalogs. This discovers Python GUI adapters and QML files.
Run `uv run python scripts/translations.py check` for read-only validation;
`build` compiles finished translations and regenerates Qt resources. Both frontend
update scripts use these commands. Do not edit generated QM files manually.

The supported language registry is `src/backend/ui_languages.py`. Add languages
there, extract catalogs, then build resources. The registry drives both language
selectors and compilation. Retain old entries' order for legacy settings migration.
English source edits belong in code, not in Weblate. Use `//:` QML translator notes
and whole messages with `.arg()` / `%n` rather than concatenated sentence fragments.
Prefer Qt locale formatting (`Number.toLocaleString(Qt.locale(), …)` in QML) for
user-facing numbers. Do not localize serialized API values, filenames or URLs.

Start with German as a pilot before inviting contributors to other languages.
Upload non-sensitive screenshots of both layouts to the relevant Weblate strings.
Glossary: **fetch** prepares a list; **download** saves media; **cleanup** removes
partial data; **resume** continues partial data. Technical protocol names stay intact.

## Self-hosted Weblate

Use `deployment/weblate/compose.yaml` on a host with at least 2 CPUs / 3 GB RAM.
See https://docs.weblate.org/en/latest/admin/install/docker.html for supported image
versions and upgrade requirements. Supply an untracked `.env` with WEBLATE_VERSION
(an explicit current supported tag), DATABASE_PASSWORD, TRANSLATION_DOMAIN,
ADMIN_EMAIL, ADMIN_PASSWORD, SMTP_HOST, SMTP_USER and SMTP_PASSWORD.
Serve the loopback port 8088 through your HTTPS reverse proxy. Keep PostgreSQL and
Valkey private. Run `docker compose config` before `docker compose up -d`.

Configure a public Porn Fetch project and a GUI component:

| Setting | Value |
| --- | --- |
| Repository | https://github.com/EchterAlsFake/Porn_Fetch.git |
| Branch | master (verify against the repository default before deployment) |
| File mask | `src/frontend/translations/ts/*.ts` |
| File format | Qt Linguist TS v2 |
| Source language | English |
| Source file / new translation template | `src/frontend/translations/ts/en.ts` |
| Push branch | `weblate-translations` |
| Version control | GitHub with pull requests enabled |
| Automatic merge | Disabled |
| Review | Enable reviews; contributors suggest, reviewers approve |
| Translation license | Repository's Porn Fetch Source-Available License 1.0 |

Register a GitHub integration with access only to this repository. Keep credentials
in Weblate, never the app or CI preview job. Enable placeholder and markup checks.
Protect the main branch and require catalog validation and maintainer review.
See https://docs.weblate.org/en/latest/admin/code-hosting.html for integration setup.

Back up the database and `/app/data` together daily and before updates. Stop Weblate
while making a consistent snapshot: `docker compose stop weblate`, dump with
`docker compose exec -T database pg_dump -U weblate weblate > backup.sql`, archive
the weblate data volume, then start Weblate. Keep encrypted off-host copies.
To restore, stop Weblate, restore the data volume and import the SQL dump into an
empty database of the same supported PostgreSQL version, then start and verify
login, catalogs and Git synchronization. Test this on an isolated host before launch.
Monitor HTTPS availability, disk space, failed background jobs and backup age.
