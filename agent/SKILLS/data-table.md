# SKILL — Data Table

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

Tables are for comparing data across multiple dimensions. If you are not comparing, use a list. If you have fewer than 3 columns, use a list. A table forces the user to scan across rows and down columns — that's only worth the cognitive cost when the relationships between columns carry meaning.

---

## When to Use Table vs List

| Use `<table>` | Use list / cards |
|---|---|
| 3+ columns of comparable data | 1–2 columns only |
| Users need to compare row-to-row | Each row is self-contained |
| Sortable/filterable data set | Static informational content |
| Numerical columns with alignment | No meaningful column comparison |
| Administrative / dashboard data | Marketing or content listings |

---

## Base Table Structure

```tsx
<div className="w-full overflow-x-auto rounded-lg border border-border">
  <table className="w-full text-sm border-collapse">
    <thead className="bg-muted/50 border-b border-border">
      <tr>
        {columns.map((col) => (
          <th
            key={col.id}
            scope="col"
            className={cn(
              "h-10 px-4 text-left align-middle font-medium text-muted-foreground",
              col.align === "right" && "text-right",
              col.align === "center" && "text-center"
            )}
          >
            {col.label}
          </th>
        ))}
      </tr>
    </thead>
    <tbody>
      {rows.map((row, i) => (
        <tr
          key={row.id}
          className="border-b border-border last:border-0 transition-colors duration-100 hover:bg-muted/30"
        >
          {columns.map((col) => (
            <td
              key={col.id}
              className={cn(
                "px-4 py-3 align-middle",
                col.align === "right" && "text-right tabular-nums",
                col.align === "center" && "text-center"
              )}
            >
              {col.render ? col.render(row) : row[col.key]}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

`tabular-nums` on numeric columns keeps digit widths consistent across rows, so numbers align correctly in right-justified columns.

---

## Sortable Columns

```tsx
function SortableHeader({ column, sortState, onSort }) {
  const isActive = sortState.column === column.id
  const direction = sortState.direction

  return (
    <th scope="col" className="h-10 px-4 text-left align-middle">
      <button
        type="button"
        onClick={() => onSort(column.id)}
        aria-sort={
          isActive
            ? direction === "asc"
              ? "ascending"
              : "descending"
            : "none"
        }
        className={cn(
          "flex items-center gap-1.5 text-xs font-medium uppercase tracking-wider",
          "transition-colors duration-150 hover:text-foreground",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-sm",
          isActive ? "text-foreground" : "text-muted-foreground"
        )}
      >
        {column.label}
        <span className="flex flex-col" aria-hidden="true">
          <ChevronUp className={cn("size-3", isActive && direction === "asc" ? "text-foreground" : "text-muted-foreground/40")} />
          <ChevronDown className={cn("size-3 -mt-1", isActive && direction === "desc" ? "text-foreground" : "text-muted-foreground/40")} />
        </span>
      </button>
    </th>
  )
}
```

`aria-sort` values must be one of: `"ascending"`, `"descending"`, `"none"`, or `"other"`. Apply to the `<th>` element, not the button inside it. The `none` value is correct for sortable-but-currently-unsorted columns. Omit `aria-sort` entirely on non-sortable columns.

---

## Row Selection

```tsx
// Select-all checkbox in thead
<th scope="col" className="w-10 px-4">
  <input
    type="checkbox"
    checked={selectedIds.size === rows.length && rows.length > 0}
    ref={(el) => {
      if (el) el.indeterminate = selectedIds.size > 0 && selectedIds.size < rows.length
    }}
    onChange={(e) => setSelectedIds(e.target.checked ? new Set(rows.map((r) => r.id)) : new Set())}
    aria-label={
      selectedIds.size === rows.length
        ? "Deselect all rows"
        : "Select all rows"
    }
    className="rounded accent-primary focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
  />
</th>

// Per-row checkbox in tbody
<td className="w-10 px-4">
  <input
    type="checkbox"
    checked={selectedIds.has(row.id)}
    onChange={(e) => {
      const next = new Set(selectedIds)
      e.target.checked ? next.add(row.id) : next.delete(row.id)
      setSelectedIds(next)
    }}
    aria-label={`Select row ${row.name}`}
    className="rounded accent-primary focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
  />
</td>
```

The `indeterminate` state (some but not all rows selected) must be set via a ref — it is not a React-controlled prop.

---

## Bulk Action Bar

Appears when one or more rows are selected:

```tsx
{selectedIds.size > 0 && (
  <div
    role="status"
    aria-live="polite"
    className={cn(
      "flex items-center gap-4 px-4 py-2.5 rounded-lg bg-primary text-primary-foreground",
      "transition-all duration-200 motion-safe:animate-in motion-safe:slide-in-from-top motion-safe:duration-200"
    )}
  >
    <span className="text-sm font-medium">
      {selectedIds.size} {selectedIds.size === 1 ? "row" : "rows"} selected
    </span>
    <div className="flex items-center gap-2 ml-auto">
      <Button
        size="sm"
        variant="secondary"
        onClick={handleBulkExport}
      >
        Export
      </Button>
      <Button
        size="sm"
        variant="destructive"
        onClick={handleBulkDelete}
      >
        Delete
      </Button>
    </div>
  </div>
)}
```

---

## Filtering and Search

```tsx
<div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-4">
  {/* Search input */}
  <div className="relative w-full sm:max-w-xs">
    <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" aria-hidden="true" />
    <label htmlFor="table-search" className="sr-only">Search</label>
    <input
      id="table-search"
      type="search"
      placeholder="Search..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="pl-9 h-9 w-full rounded-md border border-input bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
    />
  </div>

  {/* Filter chips */}
  <div className="flex items-center gap-2 flex-wrap">
    {activeFilters.map((filter) => (
      <button
        key={filter.id}
        type="button"
        onClick={() => removeFilter(filter.id)}
        aria-label={`Remove filter: ${filter.label}`}
        className="flex items-center gap-1.5 rounded-full border border-border bg-muted px-2.5 py-1 text-xs hover:bg-accent transition-colors duration-150"
      >
        {filter.label}
        <X className="size-3" aria-hidden="true" />
      </button>
    ))}
    {activeFilters.length > 0 && (
      <button
        type="button"
        onClick={clearAllFilters}
        className="text-xs text-muted-foreground hover:text-foreground transition-colors duration-150"
      >
        Clear all
      </button>
    )}
  </div>

  {/* Column visibility toggle / filter panel trigger */}
  <div className="ml-auto">
    <Button variant="outline" size="sm" className="gap-2">
      <Filter className="size-3.5" aria-hidden="true" />
      Filters
    </Button>
  </div>
</div>
```

---

## Pagination

```tsx
<nav aria-label="Table pagination" className="flex items-center justify-between py-4">
  <p className="text-sm text-muted-foreground">
    Showing <span className="font-medium text-foreground">{startItem}</span>–
    <span className="font-medium text-foreground">{endItem}</span> of{" "}
    <span className="font-medium text-foreground">{totalItems}</span>
  </p>

  <div className="flex items-center gap-1">
    <Button
      variant="outline"
      size="sm"
      onClick={() => setPage(1)}
      disabled={page === 1}
      aria-label="Go to first page"
    >
      <ChevronsLeft className="size-4" aria-hidden="true" />
    </Button>
    <Button
      variant="outline"
      size="sm"
      onClick={() => setPage(page - 1)}
      disabled={page === 1}
      aria-label="Go to previous page"
    >
      <ChevronLeft className="size-4" aria-hidden="true" />
    </Button>

    {/* Page numbers */}
    <span className="px-3 text-sm tabular-nums text-muted-foreground">
      Page {page} of {totalPages}
    </span>

    <Button
      variant="outline"
      size="sm"
      onClick={() => setPage(page + 1)}
      disabled={page === totalPages}
      aria-label="Go to next page"
    >
      <ChevronRight className="size-4" aria-hidden="true" />
    </Button>
    <Button
      variant="outline"
      size="sm"
      onClick={() => setPage(totalPages)}
      disabled={page === totalPages}
      aria-label="Go to last page"
    >
      <ChevronsRight className="size-4" aria-hidden="true" />
    </Button>
  </div>
</nav>
```

---

## Empty and Loading States

### Loading — skeleton rows

```tsx
<tbody aria-busy="true" aria-label="Loading data">
  {Array.from({ length: 5 }).map((_, i) => (
    <tr key={i} className="border-b border-border">
      {columns.map((col) => (
        <td key={col.id} className="px-4 py-3">
          <div className="h-4 rounded-md bg-muted animate-pulse" style={{ width: `${60 + Math.random() * 30}%` }} />
        </td>
      ))}
    </tr>
  ))}
</tbody>
```

Note: the `style` with `Math.random()` creates varied skeleton widths for a natural look. For SSR, use fixed percentages to avoid hydration mismatch.

### Empty state

```tsx
<tbody>
  <tr>
    <td colSpan={columns.length} className="py-16 text-center">
      <div className="flex flex-col items-center gap-3">
        <InboxIcon className="size-8 text-muted-foreground" aria-hidden="true" />
        <div>
          <p className="text-sm font-medium text-foreground">No results found</p>
          <p className="text-sm text-muted-foreground mt-1">
            {search
              ? `No items match "${search}". Try a different search term.`
              : "No items have been added yet."
            }
          </p>
        </div>
        {!search && onAdd && (
          <Button size="sm" onClick={onAdd} className="mt-2">Add item</Button>
        )}
      </div>
    </td>
  </tr>
</tbody>
```

---

## Row Actions

```tsx
<td className="px-4 py-3 text-right">
  <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <Button
        variant="ghost"
        size="icon"
        aria-label={`Actions for ${row.name}`}
      >
        <MoreHorizontal className="size-4" aria-hidden="true" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem onClick={() => onView(row)}>View</DropdownMenuItem>
      <DropdownMenuItem onClick={() => onEdit(row)}>Edit</DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem
        onClick={() => onDelete(row)}
        className="text-destructive focus:text-destructive focus:bg-destructive/10"
      >
        Delete
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</td>
```

Always anchor the dropdown `align="end"` for the last column — the dropdown opens left-aligned from the right edge, staying within viewport.

---

## Sticky Header + Scrollable Body

For long tables inside a fixed-height container:

```tsx
<div className="rounded-lg border border-border overflow-hidden">
  <div className="overflow-auto max-h-[600px]">
    <table className="w-full text-sm border-collapse">
      <thead className="sticky top-0 z-10 bg-muted/90 backdrop-blur-sm border-b border-border">
        {/* thead content */}
      </thead>
      <tbody>
        {/* tbody content */}
      </tbody>
    </table>
  </div>
</div>
```

`sticky top-0 z-10` on `<thead>` keeps column headers visible during scroll. `bg-muted/90 backdrop-blur-sm` ensures the header remains opaque/readable over scrolling rows.

---

## Responsive Behavior

Tables do not collapse gracefully below `md:`. Two strategies:

**1. Horizontal scroll (default for data tables)**
Wrap in `overflow-x-auto`. The table structure is preserved. Appropriate for dense comparative data.

**2. Card stack (for list-like tables)**
At mobile, render each row as a card with label-value pairs:

```tsx
{/* Mobile: card view */}
<div className="md:hidden flex flex-col gap-3">
  {rows.map((row) => (
    <div key={row.id} className="rounded-lg border border-border p-4 flex flex-col gap-2">
      {columns.filter((c) => c.key !== "actions").map((col) => (
        <div key={col.id} className="flex items-center justify-between">
          <span className="text-xs font-medium text-muted-foreground">{col.label}</span>
          <span className="text-sm text-foreground">{row[col.key]}</span>
        </div>
      ))}
    </div>
  ))}
</div>

{/* Desktop: table view */}
<div className="hidden md:block overflow-x-auto">
  <table className="w-full ...">...</table>
</div>
```

---

## Accessibility

- `<table>` is the correct element — never recreate a table with divs and CSS grid
- `<th scope="col">` on all column headers; `<th scope="row">` if the first column is a row identifier
- `<caption>` or `aria-labelledby` on the table: describes the data set to screen readers
- `aria-sort` on sortable column headers (values: `"ascending"`, `"descending"`, `"none"`)
- `aria-busy="true"` on `<tbody>` while data is loading
- `aria-live="polite"` on result count / status messages (filter results, sort changes)
- Row checkboxes: `aria-label="Select row [identifier]"` — not "Select row"
- Select-all checkbox: explicit `aria-label` that changes with state
- Pagination nav: `aria-label="Table pagination"` on the `<nav>`, descriptive `aria-label` on each page button

---

## Common Pitfalls

- **Div table:** never replace `<table>` with grid divs for tabular data — loses all semantic and accessibility structure
- **No `scope` on headers:** without `scope="col"`, screen readers cannot associate cell content with column headers
- **Number columns without `tabular-nums`:** numbers misalign when digit widths vary (e.g., 1 is narrower than 8 in proportional fonts)
- **Loading state shows empty state:** the loading skeleton and the empty state are mutually exclusive. Show skeleton while fetching, empty state only after the fetch resolves with zero results.
- **Uncapped table height:** a table without `max-h` and `overflow-y-auto` inside a fixed layout will push everything below it off-screen
- **"Actions" column too narrow:** the ellipsis button column must be wide enough to click comfortably. `w-12` minimum, `w-16` preferred.
- **No `caption`:** all tables need a programmatic description. Use `<caption className="sr-only">` if a visible caption doesn't fit the design.
