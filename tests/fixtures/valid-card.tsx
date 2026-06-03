export function ValidCard() {
  return (
    <div
      data-slot="card"
      className="rounded-lg border bg-card text-card-foreground shadow-sm"
    >
      <div className="flex flex-col gap-1.5 p-6">
        <h3 className="text-base font-semibold leading-tight">Title</h3>
        <p className="text-sm text-muted-foreground">Description</p>
      </div>
      <div className="p-6 pt-0">
        <p className="text-sm text-foreground">Body content</p>
      </div>
    </div>
  );
}
