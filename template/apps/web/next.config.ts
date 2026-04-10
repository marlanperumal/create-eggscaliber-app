{% if use_sentry %}
import { withSentryConfig } from "@sentry/nextjs"
{% endif %}
import type { NextConfig } from "next"

const nextConfig: NextConfig = {}

{% if use_sentry %}
export default withSentryConfig(nextConfig, {
  org: "{{ project_name }}",
  project: "{{ project_name }}-web",
  silent: !process.env.CI,
  widenClientFileUpload: true,
  automaticVercelMonitors: true,
})
{% else %}
export default nextConfig
{% endif %}
