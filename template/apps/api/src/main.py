{% if use_sentry %}
import sentry_sdk
{% endif %}
from fastapi import FastAPI

from src.config import settings
{% if use_sentry %}
from src.routes import health, sentry
{% else %}
from src.routes import health
{% endif %}

{% if use_sentry %}
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=0.1,
    )

{% endif %}
app = FastAPI(title="{{ project_name }} API", version="0.1.0")

app.include_router(health.router, prefix="/api/v1")
{% if use_sentry %}
app.include_router(sentry.router, prefix="/api/v1")
{% endif %}
