"""Tests for the post_copy hook: SETUP.md generation and terminal summary."""
import pytest
from hooks.post_copy import get_answers, generate_setup_md, print_summary


# ── get_answers ───────────────────────────────────────────────────────────────

def test_get_answers_defaults_when_env_unset(monkeypatch):
    for key in ["project_name", "use_clerk", "use_sentry", "use_posthog",
                "use_chromatic", "use_marimo", "use_vercel", "use_render", "use_neon"]:
        monkeypatch.delenv(key, raising=False)
    answers = get_answers()
    assert answers["project_name"] == "my-app"
    assert answers["use_clerk"] is False
    assert answers["use_sentry"] is False


def test_get_answers_parses_true(monkeypatch):
    monkeypatch.setenv("project_name", "my-project")
    monkeypatch.setenv("use_clerk", "true")
    monkeypatch.setenv("use_sentry", "True")
    answers = get_answers()
    assert answers["project_name"] == "my-project"
    assert answers["use_clerk"] is True
    assert answers["use_sentry"] is True


def test_get_answers_parses_false(monkeypatch):
    monkeypatch.setenv("use_posthog", "false")
    monkeypatch.setenv("use_render", "False")
    answers = get_answers()
    assert answers["use_posthog"] is False
    assert answers["use_render"] is False


# ── generate_setup_md ─────────────────────────────────────────────────────────

def _answers(**overrides):
    base = {
        "project_name": "test-app",
        "use_clerk": False,
        "use_sentry": False,
        "use_posthog": False,
        "use_chromatic": False,
        "use_marimo": False,
        "use_vercel": False,
        "use_render": False,
        "use_neon": False,
    }
    return {**base, **overrides}


def test_setup_md_always_includes_prerequisites():
    content = generate_setup_md(_answers())
    assert "Docker Desktop" in content
    assert "https://docs.docker.com/get-docker/" in content
    assert "https://docs.astral.sh/uv/" in content
    assert "https://pnpm.io/installation" in content
    assert "https://just.systems" in content
    assert "just setup" in content


def test_setup_md_includes_only_selected_dev_integrations():
    content = generate_setup_md(_answers(use_clerk=True, use_posthog=True))
    assert "### Clerk" in content
    assert "### PostHog" in content
    assert "### Sentry" not in content
    assert "### Chromatic" not in content
    assert "### Marimo" not in content


def test_setup_md_excludes_all_dev_integrations_when_none_selected():
    content = generate_setup_md(_answers())
    assert "## 2. Development Integrations" not in content


def test_setup_md_includes_only_selected_deployment_integrations():
    content = generate_setup_md(_answers(use_vercel=True, use_neon=True, use_render=True))
    assert "### Vercel" in content
    assert "### Render" in content
    assert "### Neon" in content


def test_setup_md_excludes_deployment_section_when_none_selected():
    content = generate_setup_md(_answers())
    assert "## 3. Deployment" not in content


def test_setup_md_secrets_checklist_shows_only_relevant_secrets():
    content = generate_setup_md(_answers(use_chromatic=True, use_vercel=True))
    assert "CHROMATIC_PROJECT_TOKEN" in content
    assert "VERCEL_TOKEN" in content
    assert "RENDER_API_KEY" not in content


def test_setup_md_secrets_checklist_absent_when_no_secrets_needed():
    content = generate_setup_md(_answers(use_marimo=True))
    assert "GitHub Actions Secrets" not in content


def test_setup_md_uses_project_name_in_heading():
    content = generate_setup_md(_answers(project_name="my-cool-app"))
    assert "# my-cool-app Setup Guide" in content


# ── print_summary ─────────────────────────────────────────────────────────────

def test_print_summary_shows_selected_integrations(capsys):
    print_summary(_answers(use_clerk=True, use_sentry=True))
    captured = capsys.readouterr()
    assert "Clerk" in captured.out
    assert "Sentry" in captured.out
    assert "PostHog" not in captured.out


def test_print_summary_shows_config_needed_for_clerk(capsys):
    print_summary(_answers(use_clerk=True))
    captured = capsys.readouterr()
    assert "CLERK_SECRET_KEY" in captured.out


def test_print_summary_shows_next_steps(capsys):
    print_summary(_answers(project_name="test-app"))
    captured = capsys.readouterr()
    assert "cd test-app" in captured.out
    assert "just setup" in captured.out
    assert "SETUP.md" in captured.out


def test_print_summary_no_config_section_when_no_external_config_needed(capsys):
    print_summary(_answers(use_marimo=True))
    captured = capsys.readouterr()
    assert "needing config" not in captured.out
