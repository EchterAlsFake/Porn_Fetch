# Porn Fetch contributor instructions

- Keep Qt out of CLI, shared, licensing, and database core code. Use PySide6 for
  GUI work and use async workers with cooperative cancellation.
- Use maintained dependencies, prefer simple implementations, and focus tests
  on the requested behavior and relevant regressions.

<!-- knowledge:begin -->
## Private project knowledge
<!-- knowledge-project: porn-fetch -->

For substantial work, open the matching topic with `read_context_file` using
its full path and project prefix. For an unfamiliar task, open
`porn-fetch/canonical/project.md` or run a project-scoped `search_knowledge`.
Resume with `get_recent_handoffs`, filtered by branch when known. Read the
`infrastructure` brief for deployment or named-device work. Pass
`include_metadata=true` for direct payment and infrastructure note lookups.
Recheck flagged or unverified notes before relying on them. If the MCP is
unavailable, use the checked-out code and maintained repository docs.

| Task | Private topic path |
| --- | --- |
| New UI features, QML, settings, notifications, Android layouts | `porn-fetch/canonical/ui.md` |
| Providers, pagination, creator subscriptions, SNI proxy, downloads | `porn-fetch/canonical/backend.md` |
| Packaging, updates, builds, releases, tests | `porn-fetch/canonical/releases.md` |
| Marketing, outreach, product claims | `porn-fetch/canonical/marketing.md` |
| Payment processing, checkout, PSPs, webhooks, refunds, server-side licensing | `porn-fetch-server/canonical/psp.md` |

Keep the project index short and use one focused note per topic. Split notes
before 500 words and link related notes by path. Keep long audits and source
material in references. Keep internal notes and work logs out of Git.

After meaningful work, call `save_handoff` for `porn-fetch` with changes,
checks and the next action. Keep each field to one or two short sentences.
Include branch and commit when useful. Reuse the UUID on retry. Keep secrets,
transcripts and uncommitted code out. Bring canonical changes to the owner.
<!-- knowledge:end -->
