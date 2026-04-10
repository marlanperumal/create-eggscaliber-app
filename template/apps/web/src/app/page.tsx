export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">{{ project_name }}</h1>
      <p className="text-muted-foreground mt-4">{{ project_description }}</p>
    </main>
  )
}
