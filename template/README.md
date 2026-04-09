# {{ project_name }}

{{ project_description }}

## Getting started

See [SETUP.md](SETUP.md) for full setup instructions including prerequisites and
integration configuration.

### Quick start (after completing SETUP.md)

```bash
just dev       # start API (localhost:8000) + web (localhost:3000) concurrently
just test      # run all tests
just storybook # component explorer (localhost:6006)
```

See `just --list` for all available commands.

## Keeping up with the template

This project was scaffolded from
[create-eggscaliber-app](https://github.com/marlanperumal/create-eggscaliber-app).
To pull in template improvements:

```bash
uvx copier update
```

Run from the project root. Copier re-applies template changes while preserving your
project-specific modifications.

**Important:** Do not delete `.copier-answers.yml` — it records your original answers and
template ref, and is required for `copier update` to work correctly.

To pin an update to a specific template version:

```bash
uvx copier update --vcs-ref=v1.x.x
```
