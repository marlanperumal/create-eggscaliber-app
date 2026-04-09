# Default: list commands
default:
    @just --list

# Scaffold a test project with all integrations (non-interactive)
test:
    rm -rf /tmp/cea-test-output
    uvx copier copy . /tmp/cea-test-output \
        --data project_name=test-app \
        --data project_description="Test application" \
        --data use_clerk=true \
        --data use_sentry=true \
        --data use_posthog=true \
        --data use_chromatic=true \
        --data use_marimo=true \
        --data use_vercel=true \
        --data use_render=true \
        --data use_neon=true \
        --defaults --overwrite
    @echo "✔ Template scaffolded to /tmp/cea-test-output"

# Scaffold interactively to ./test-output for manual inspection
dev:
    rm -rf ./test-output
    uvx copier copy . ./test-output

# Run pytest unit tests
unit:
    uv run pytest tests/ -v
