{% if use_posthog %}
import { PostHogPageView, PostHogProvider } from "@posthog/next"
{% endif %}
{% if use_clerk %}
import { ClerkProvider } from "@clerk/nextjs"
{% endif %}
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "{{ project_name }}",
  description: "{{ project_description }}",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
{% if use_clerk %}
    <ClerkProvider>
{% endif %}
    <html lang="en">
      <body className={inter.className}>
{% if use_posthog %}
        <PostHogProvider
          clientOptions={{ '{{' }} api_host: "/ingest", debug: process.env.NODE_ENV === "development" {{ '}}' }}
          bootstrapFlags
        >
          <PostHogPageView />
          {children}
        </PostHogProvider>
{% else %}
        {children}
{% endif %}
      </body>
    </html>
{% if use_clerk %}
    </ClerkProvider>
{% endif %}
  )
}
