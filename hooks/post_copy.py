#!/usr/bin/env python3
"""Post-copy hook: generates SETUP.md and prints terminal summary."""
import os
from pathlib import Path


def get_answers() -> dict:
    """Read Copier answers from environment variables (set by Copier before running hook)."""
    bool_keys = [
        "use_clerk", "use_sentry", "use_posthog", "use_chromatic",
        "use_marimo", "use_vercel", "use_render", "use_neon",
    ]
    answers: dict = {"project_name": os.environ.get("project_name", "my-app")}
    for key in bool_keys:
        answers[key] = os.environ.get(key, "false").lower() == "true"
    return answers


def generate_setup_md(answers: dict) -> str:
    """Generate SETUP.md content tailored to selected integrations."""
    project_name = answers["project_name"]
    sections: list[str] = [f"# {project_name} Setup Guide\n"]

    # ── Section 1: Local Development (always included) ────────────────────────
    sections.append("""## 1. Local Development

### Prerequisites

Install these before running `just setup`:

- [Docker Desktop](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- [pnpm](https://pnpm.io/installation) — Node package manager
- [just](https://just.systems/man/en/packages.html) — command runner

### First run

```bash
cp .env.example .env.local
# Fill in any required integration keys (see sections below)
just setup
just dev
```
""")

    # ── Section 2: Development Integrations ───────────────────────────────────
    dev_sections: list[str] = []

    if answers["use_clerk"]:
        dev_sections.append("""### Clerk

1. Create an account at [clerk.com](https://clerk.com) and create an application.
2. Copy keys to `.env.local`:
   - `CLERK_SECRET_KEY`
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
3. Configure redirect URLs in the Clerk dashboard.
""")

    if answers["use_sentry"]:
        dev_sections.append("""### Sentry

1. Create two projects at [sentry.io](https://sentry.io): one Python, one Next.js.
2. Run the Sentry wizard in `apps/web/`:
   ```bash
   cd apps/web && npx @sentry/wizard@latest -i nextjs
   ```
3. Set `SENTRY_DSN` in `.env.local` (API) and in your hosting platform env vars.
""")

    if answers["use_posthog"]:
        dev_sections.append("""### PostHog

1. Create an account at [posthog.com](https://posthog.com).
2. Run the PostHog wizard in `apps/web/` (verify command against current docs):
   ```bash
   cd apps/web && npx @posthog/wizard@latest
   ```
3. Set `NEXT_PUBLIC_POSTHOG_KEY` in `.env.local`.
""")

    if answers["use_chromatic"]:
        dev_sections.append("""### Chromatic

1. Create an account at [chromatic.com](https://www.chromatic.com) and link your repo.
2. Publish your first build:
   ```bash
   cd apps/web && npx chromatic --project-token=<your-token>
   ```
3. Add `CHROMATIC_PROJECT_TOKEN` to GitHub Actions secrets.
""")

    if answers["use_marimo"]:
        dev_sections.append("""### Marimo

No external account needed. Start the notebook server with:

```bash
just notebook
```
""")

    if dev_sections:
        sections.append("## 2. Development Integrations\n")
        sections.extend(dev_sections)

    # ── Section 3: Deployment ─────────────────────────────────────────────────
    deploy_sections: list[str] = []

    if answers["use_vercel"]:
        deploy_sections.append("""### Vercel (web)

1. Import your repo at [vercel.com](https://vercel.com) — set the root directory to
   `apps/web`. Vercel will deploy automatically on push to master via GitHub integration.
2. Set all `NEXT_PUBLIC_*` and auth-related env vars in the Vercel dashboard.
""")

    if answers["use_render"]:
        deploy_sections.append("""### Render (API)

1. Create a Web Service at [render.com](https://render.com) — set the root directory to
   `apps/api`. Render deploys automatically on push to master via GitHub integration.
2. Set `DATABASE_URL` and all API env vars in the Render environment.
""")

    if answers["use_neon"]:
        db_target = "Render" if answers["use_render"] else "your hosting platform"
        deploy_sections.append(f"""### Neon (managed Postgres)

1. Create a project at [neon.tech](https://neon.tech).
2. Replace `DATABASE_URL` in {db_target} with the Neon connection string.
3. Run migrations against production before first deploy:
   ```bash
   DATABASE_URL=<neon-connection-string> just db-migrate
   ```
""")

    if deploy_sections:
        sections.append("## 3. Deployment\n")
        sections.extend(deploy_sections)

    # ── Section 4: GitHub Actions Secrets Checklist ───────────────────────────
    secrets: list[tuple[str, str]] = []
    if answers["use_chromatic"]:
        secrets.append(("CHROMATIC_PROJECT_TOKEN", "Chromatic step in `deploy.yml`"))
    if answers["use_vercel"]:
        secrets.extend([
            ("VERCEL_TOKEN", "deploy.yml — Vercel deploy"),
            ("VERCEL_ORG_ID", "deploy.yml — Vercel deploy"),
            ("VERCEL_PROJECT_ID", "deploy.yml — Vercel deploy"),
        ])
    if answers["use_render"]:
        secrets.extend([
            ("RENDER_API_KEY", "deploy.yml — Render deploy"),
            ("RENDER_SERVICE_ID", "deploy.yml — Render deploy"),
        ])

    if secrets:
        checklist = "## 4. GitHub Actions Secrets Checklist\n\n"
        checklist += "| Secret | Required by |\n|--------|-------------|\n"
        for secret, required_by in secrets:
            checklist += f"| `{secret}` | {required_by} |\n"
        checklist += "\nAdd these at: GitHub repo → Settings → Secrets and variables → Actions\n"
        sections.append(checklist)

    return "\n".join(sections)


def print_summary(answers: dict) -> None:
    """Print a concise post-scaffold summary to the terminal."""
    project_name = answers["project_name"]

    integration_keys = [
        ("use_clerk", "Clerk"),
        ("use_sentry", "Sentry"),
        ("use_posthog", "PostHog"),
        ("use_chromatic", "Chromatic"),
        ("use_marimo", "Marimo"),
        ("use_vercel", "Vercel"),
        ("use_render", "Render"),
        ("use_neon", "Neon"),
    ]
    selected = [name for key, name in integration_keys if answers[key]]

    config_needed: list[str] = []
    if answers["use_clerk"]:
        config_needed.append(
            "-> Clerk    CLERK_SECRET_KEY, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY  (.env.local)"
        )
    if answers["use_sentry"]:
        config_needed.append(
            "-> Sentry   SENTRY_DSN  (.env.local)  +  run: npx @sentry/wizard@latest -i nextjs"
        )
    if answers["use_posthog"]:
        config_needed.append(
            "-> PostHog  NEXT_PUBLIC_POSTHOG_KEY  (.env.local)"
        )
    if answers["use_chromatic"] or answers["use_vercel"] or answers["use_render"]:
        config_needed.append(
            "-> GitHub Actions secrets needed — see SETUP.md § GitHub Actions Secrets Checklist"
        )

    print("\nProject scaffolded\n")

    if selected:
        print(f"  Integrations: {', '.join(selected)}\n")

    print("  Next steps:")
    print(f"    cd {project_name}")
    print("    just setup\n")

    if config_needed:
        print("  Integrations needing config before `just setup`:")
        for line in config_needed:
            print(f"    {line}")
        print()

    print("  Full instructions: SETUP.md\n")


if __name__ == "__main__":
    answers = get_answers()
    setup_content = generate_setup_md(answers)
    dst = Path(os.environ.get("SETUP_MD_DST", ".")).resolve()
    (dst / "SETUP.md").write_text(setup_content)
    print_summary(answers)
