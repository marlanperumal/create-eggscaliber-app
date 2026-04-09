# create-eggscaliber-app

Scaffold a new full-stack project based on [eggscaliber-lite](https://github.com/marlanperumal/eggscaliber-lite)
in minutes. Built on [Copier](https://copier.readthedocs.io/).

## Usage

```bash
uvx copier copy gh:marlanperumal/create-eggscaliber-app ./my-project
```

Copier will prompt for:

- **Project name** — used in package names and database names
- **Project description**
- **Development integrations** — Clerk (auth), Sentry (errors), PostHog (analytics), Chromatic (visual testing), Marimo (notebooks)
- **Deployment integrations** — Vercel (web), Render (API), Neon (managed Postgres)

After scaffolding, follow the generated `SETUP.md` in your new project.

## Pin to a specific version

```bash
uvx copier copy --vcs-ref=v1.0.0 gh:marlanperumal/create-eggscaliber-app ./my-project
```

## Local testing

```bash
git clone https://github.com/marlanperumal/create-eggscaliber-app
cd create-eggscaliber-app
uv sync
just dev   # interactive scaffold to ./test-output
just test  # scaffold with all integrations to /tmp/cea-test-output
just unit  # run pytest unit tests
```

## Releasing a new version

```bash
git tag v1.x.x
git push --tags
```

No registry publish needed — users pull directly from GitHub.

## Adding a new integration

1. Add a `use_<name>:` question to `copier.yaml`
2. Add `_exclude` entries for files that should be omitted when the integration is not selected
3. Add Jinja2 conditionals to any shared files that need modifying
4. Add a section to `generate_setup_md()` in `hooks/post_copy.py`
5. Add a line to `print_summary()` for config-needed entries if applicable
6. Add tests to `tests/test_post_copy.py`
7. Run `just test` and `just unit` to verify
8. Tag a new release
