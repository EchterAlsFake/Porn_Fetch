# Translations

**Porn Fetch is English-only. It does not have translations at the moment.**
The translation files and Weblate integration are unfinished. The language
selector is disabled. Provider content language is a separate setting.

Older German, Chinese, French and Italian catalogs remain in the repository
for future work. They are not shipped as working interface translations.
Please contact the maintainer before starting a large translation contribution.
The planned service is [Weblate](https://translations.echteralsfake.me/).

## For maintainers

After changing interface text, use the development environment from the
[developer guide](FOR_DEVELOPERS.md):

```sh
uv run --no-sync python scripts/translations.py extract
uv run --no-sync python scripts/translations.py check
uv run --no-sync python scripts/translations.py build
```

Commit the TS catalogs and generated resources. Keep whole sentences together
and preserve placeholders such as `%1`, `%n` and `${title}`. Do not translate
URLs, product names or stored API values. The locale registry is
`src/backend/ui_languages.py`; retain its order for old settings migration.
`ui_translation.py` currently forces English even when an old preference exists.

Before enabling another language, finish and review its catalog, restore the
language selector and runtime switching, then test both desktop and mobile
layouts. Check long text, plural forms, keyboard navigation and screen readers.
The translation preview workflow currently previews the English interface.

The unfinished self-hosted service configuration is in `deployment/weblate/`.
Follow the [Weblate Docker guide](https://docs.weblate.org/en/latest/admin/install/docker.html)
for deployment and upgrades. Keep credentials outside Git, require reviewed
pull requests, and back up both the database and application data.
