# SKILL — Drag and Drop

Extends DESIGN.md. Works alongside any STYLES/ file. Never overrides CONFIG.md or METHOD.md.

---

## Core Principle

Drag-and-drop is a direct manipulation paradigm: the user picks up an object, moves it through space, and drops it to produce an effect. Done well, it enables kanban boards, sortable lists, file uploads, and spatial organisation tools. Done poorly, it produces accidental drops, broken mobile behaviour, and drag events that conflict with native scroll.

The browser's native HTML5 Drag and Drop API (`draggable`, `ondragstart`, `ondrop`) was designed for cross-application drag (file from Finder into browser) — it does not fire on touch devices, cannot style the drag ghost, and has no activation constraint controls. **Always bypass it for in-app UI** and build on the **Pointer Events API** instead.

---

## When to Use

- Sortable lists where order is meaningful (priority queues, ranked items)
- Kanban boards (card movement across columns)
- File upload zones (drag files from OS into a drop target)
- Builder interfaces (drag components onto a canvas)
- Any interface where spatial rearrangement is the primary interaction

Do not use as the **only** way to reorder or place items — keyboard and touch users require an alternative path. Always provide drag as an enhancement over a functional base interaction (buttons, select menus).

---

## Technical Foundation: Pointer Events API

Pointer Events unify mouse, touch, and pen input through a single event model:

| Input | Old events | Pointer Events |
|---|---|---|
| Mouse | `mousedown`, `mousemove`, `mouseup` | `pointerdown`, `pointermove`, `pointerup` |
| Touch | `touchstart`, `touchmove`, `touchend` | `pointerdown`, `pointermove`, `pointerup` |
| Pen/stylus | (inconsistent) | `pointerdown`, `pointermove`, `pointerup` |

Two CSS rules are required on every draggable element:

```css
.draggable {
  touch-action: none;  /* prevents browser scroll/zoom capturing touch before drag handler */
  user-select: none;   /* prevents text selection during drag */
}
```

`touch-action: none` should be limited to the grab handle when possible — this preserves scrollability on the card body for touch users.

---

## Activation Constraints

Accidental drag activation is the most common drag UX failure. A user trying to click a button on a card should not trigger a drag. Prevent this with constraints:

| Input | Constraint type | Recommended values |
|---|---|---|
| Mouse (with grab handle) | Immediate | 0px, 0ms |
| Mouse (full-card drag) | Distance | 5px movement |
| Touch | Delay + tolerance | 250ms hold, 5px tolerance |
| Pen/stylus | Delay + tolerance | 200ms hold, 10px tolerance |

The delay for touch is not optional — without it, every tap that starts a long-press becomes a drag activation.

---

## dnd-kit (React)

The current standard for React drag-and-drop. Built on Pointer Events with zero HTML5 DnD API dependency. Modular:

```
@dnd-kit/core          — DndContext, sensors, collision detection, DragOverlay
@dnd-kit/sortable      — sortable list and grid preset
@dnd-kit/modifiers     — snap-to-grid, axis lock, viewport constraint
@dnd-kit/accessibility — ARIA announcements, keyboard navigation
```

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/modifiers @dnd-kit/utilities
```

---

## Sortable List

```tsx
import {
  DndContext,
  closestCenter,
  PointerSensor,
  KeyboardSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from "@dnd-kit/core"
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
  arrayMove,
  sortableKeyboardCoordinates,
} from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { GripVertical } from "lucide-react"
import { cn } from "@/lib/utils"

// Individual sortable item — grab handle variant
interface SortableItemProps {
  id: string
  children: React.ReactNode
}

function SortableItem({ id, children }: SortableItemProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    setActivatorNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "flex items-center gap-2 rounded-lg border border-border bg-card p-3",
        "transition-shadow duration-200",
        isDragging && "opacity-40 shadow-lg"
      )}
    >
      {/* Grab handle — only this area initiates drag */}
      <button
        ref={setActivatorNodeRef}
        {...attributes}
        {...listeners}
        aria-label="Drag to reorder"
        className={cn(
          "shrink-0 cursor-grab rounded text-muted-foreground active:cursor-grabbing",
          "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none",
          "hover:text-foreground"
        )}
      >
        <GripVertical className="h-4 w-4" aria-hidden="true" />
      </button>
      <div className="flex-1">{children}</div>
    </div>
  )
}

// Parent sortable list
interface SortableListProps<T extends { id: string }> {
  items: T[]
  onReorder: (items: T[]) => void
  renderItem: (item: T) => React.ReactNode
}

export function SortableList<T extends { id: string }>({
  items,
  onReorder,
  renderItem,
}: SortableListProps<T>) {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: { distance: 5 },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  )

  function handleDragEnd({ active, over }: DragEndEvent) {
    if (!over || active.id === over.id) return
    const oldIndex = items.findIndex(i => i.id === active.id)
    const newIndex = items.findIndex(i => i.id === over.id)
    onReorder(arrayMove(items, oldIndex, newIndex))
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        <ul className="space-y-2" role="list" aria-label="Sortable list">
          {items.map(item => (
            <li key={item.id}>
              <SortableItem id={item.id}>
                {renderItem(item)}
              </SortableItem>
            </li>
          ))}
        </ul>
      </SortableContext>
    </DndContext>
  )
}
```

---

## DragOverlay: Styled Ghost

The `DragOverlay` component renders the drag ghost in a portal at the document root — independent of any `overflow: hidden` container. Without it, dragging a card outside its parent clips the ghost.

The source item fades in place while the overlay follows the cursor:

```tsx
import { DndContext, DragOverlay, DragStartEvent, DragEndEvent } from "@dnd-kit/core"
import { useState } from "react"

function KanbanBoard() {
  const [activeId, setActiveId] = useState<string | null>(null)

  function handleDragStart({ active }: DragStartEvent) {
    setActiveId(String(active.id))
  }

  function handleDragEnd({ active, over }: DragEndEvent) {
    setActiveId(null)
    if (over && active.id !== over.id) {
      // reorder logic
    }
  }

  const activeItem = items.find(i => i.id === activeId)

  return (
    <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
      {/* columns and sortable contexts */}

      <DragOverlay>
        {activeItem ? (
          <KanbanCard
            item={activeItem}
            className="rotate-1 shadow-xl opacity-95"  // visual cue it is lifted
          />
        ) : null}
      </DragOverlay>
    </DndContext>
  )
}
```

The `rotate-1 shadow-xl` on the overlay card is the standard convention for communicating "this object is being carried."

---

## Collision Detection

Choose the algorithm based on layout:

| Algorithm | Use case |
|---|---|
| `closestCenter` | Sorted lists — activates when drag point crosses the midpoint of another item |
| `closestCorners` | Grids — uses corner proximity rather than center; better for wide/tall items |
| `rectIntersection` | Large drop zones (columns, canvas areas) — activates on any overlap |

```tsx
import { closestCenter, closestCorners, rectIntersection } from "@dnd-kit/core"

<DndContext collisionDetection={closestCenter}>    {/* vertical lists */}
<DndContext collisionDetection={closestCorners}>  {/* card grids */}
<DndContext collisionDetection={rectIntersection}> {/* kanban columns */}
```

---

## Modifiers

```tsx
import {
  restrictToVerticalAxis,
  restrictToHorizontalAxis,
  restrictToWindowEdges,
  restrictToParentElement,
  snapCenterToCursor,
} from "@dnd-kit/modifiers"

// Lock to one axis
<DndContext modifiers={[restrictToVerticalAxis]}>

// Prevent drag outside viewport
<DndContext modifiers={[restrictToWindowEdges]}>

// Combine: vertical-only + stay in window
<DndContext modifiers={[restrictToVerticalAxis, restrictToWindowEdges]}>
```

---

## Touch Configuration

Touch requires a delay-based activation constraint — distance-only activation causes every scroll attempt in a draggable list to become a drag:

```tsx
import { PointerSensor, TouchSensor, useSensor, useSensors } from "@dnd-kit/core"

const sensors = useSensors(
  useSensor(PointerSensor, {
    activationConstraint: { distance: 5 },
  }),
  useSensor(TouchSensor, {
    activationConstraint: {
      delay: 250,      // 250ms hold required on touch
      tolerance: 5,    // 5px of movement allowed during delay without cancelling
    },
  })
)
```

---

## Grab Handle vs. Full-Card Drag

**Grab handle** — a dedicated drag icon is the only initiating area:
- Preserves text selection and link-clicking on the card body
- Makes draggability explicitly visible
- Correct default for data-dense items: table rows, task lists, settings items

**Full-card drag** — the entire card surface initiates drag:
- Simpler, more obvious for visual or media-focused cards
- Requires `user-select: none` on the card — no text selection
- Works well for kanban cards, image tiles, icon-based items

For full-card drag, apply `listeners` and `attributes` to the outer `setNodeRef` div rather than a separate handle ref.

---

## Source Item Appearance During Drag

Three standard patterns — choose per context:

| Pattern | Code | Best for |
|---|---|---|
| **Fade in place** | `isDragging && "opacity-40"` | Most cases; ghost overlays faded source |
| **Hide entirely** | `isDragging && "opacity-0"` | Creates a "hole" showing where item lived |
| **Skeleton placeholder** | Replace content with `bg-muted animate-pulse` | When the empty slot needs to be prominent |

```tsx
// Skeleton placeholder pattern
{isDragging ? (
  <div className="h-16 rounded-lg border border-dashed border-border bg-muted" aria-hidden="true" />
) : (
  <div ref={setNodeRef} style={style}>{children}</div>
)}
```

---

## File Upload Drop Zone

```tsx
import { useState, useCallback } from "react"
import { Upload } from "lucide-react"
import { cn } from "@/lib/utils"

interface DropZoneProps {
  onFiles: (files: File[]) => void
  accept?: string
  multiple?: boolean
}

export function DropZone({ onFiles, accept, multiple = true }: DropZoneProps) {
  const [isDragOver, setIsDragOver] = useState(false)

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragOver(false)
      const files = Array.from(e.dataTransfer.files)
      if (files.length) onFiles(files)
    },
    [onFiles]
  )

  return (
    <label
      onDrop={handleDrop}
      onDragOver={e => { e.preventDefault(); setIsDragOver(true) }}
      onDragLeave={() => setIsDragOver(false)}
      className={cn(
        "flex cursor-pointer flex-col items-center justify-center gap-3",
        "rounded-xl border-2 border-dashed p-10 text-center",
        "transition-colors duration-200",
        isDragOver
          ? "border-primary bg-primary/5 text-primary"
          : "border-border text-muted-foreground hover:border-primary/50 hover:bg-accent/50"
      )}
    >
      <Upload className="h-8 w-8" aria-hidden="true" />
      <div>
        <p className="text-sm font-medium text-foreground">
          Drop files here or <span className="text-primary underline">browse</span>
        </p>
        {accept && (
          <p className="mt-1 text-xs text-muted-foreground">{accept}</p>
        )}
      </div>
      <input
        type="file"
        className="sr-only"
        accept={accept}
        multiple={multiple}
        onChange={e => {
          const files = Array.from(e.target.files ?? [])
          if (files.length) onFiles(files)
        }}
        aria-label="Upload files"
      />
    </label>
  )
}
```

---

## Accessibility

Drag-and-drop without a keyboard alternative is an accessibility blocker. `@dnd-kit/core`'s `KeyboardSensor` provides full keyboard reordering with zero additional work:

- **Space** or **Enter** — pick up the focused item
- **Arrow keys** — move the item through valid positions
- **Space** or **Enter** — drop at current position
- **Escape** — cancel drag and return to original position

ARIA live region announcements are emitted automatically by dnd-kit when using `KeyboardSensor`:

```tsx
// Custom announcements if needed
const announcements = {
  onDragStart: ({ active }) => `Picked up item ${active.id}`,
  onDragOver: ({ active, over }) =>
    over ? `Item ${active.id} is over position ${over.id}` : "Not over a droppable",
  onDragEnd: ({ active, over }) =>
    over ? `Item ${active.id} dropped at position ${over.id}` : "Item returned to original position",
  onDragCancel: () => "Drag cancelled",
}

<DndContext accessibility={{ announcements }}>
```

Screen readers receive spatial feedback like: "Picked up item 3 of 7", "Item moved to position 2 of 7", "Item dropped at position 2 of 7."

---

## Performance

- dnd-kit recalculates collision detection on every `pointermove` — for lists of 100+ items, avoid heavy DOM measurements in `onDragOver`
- `DragOverlay` uses `transform: translate()` — GPU-composited, no reflow
- For lists of 500+ items, virtualise with `@tanstack/virtual` — dnd-kit has documented patterns for this integration
- Keep `onDragOver` callbacks lightweight — state updates here run at 60fps

---

## Common Pitfalls

- **No touch delay** — omitting the 250ms hold constraint means every scroll in a touch draggable list tries to drag. This is the most common mobile bug.
- **No keyboard alternative** — drag-only is an accessibility failure. `KeyboardSensor` takes minutes to add and provides full compliance.
- **DragOverlay inside overflow:hidden** — not using `DragOverlay` means the drag ghost clips when the source is inside any clipped container. Always use `DragOverlay` for production drag implementations.
- **`touch-action: none` on full card** — prevents scrolling within the card. Apply only to the grab handle to preserve scroll on the card body.
- **Full-card drag with text content** — without `user-select: none`, double-click or drag on text selects it instead of dragging. Always pair full-card drag with `select-none`.
- **Wrong collision algorithm for layout** — using `closestCenter` in a grid produces jittery reordering for wide cards. Match algorithm to layout type.
- **Forgetting `arrayMove`** — computing new order manually from drag indices is error-prone. Always use dnd-kit's `arrayMove` utility.
