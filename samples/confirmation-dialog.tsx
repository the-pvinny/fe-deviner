export function ConfirmationDialog({
  open,
  onClose,
  onConfirm,
  itemName,
  isDeleting = false,
}: {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  itemName: string;
  isDeleting?: boolean;
}) {
  const dialogRef = useRef(null);

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;

    if (!open) return;

    document.body.style.overflow = "hidden";

    const getFocusable = () =>
      Array.from(
        dialogRef.current?.querySelectorAll(
          "button, [href], input, select, textarea, [tabindex]:not([tabindex=\"-1\"])"
        ) ?? []
      ).filter((el) => !el.hasAttribute("disabled"));

    const frame = requestAnimationFrame(() => getFocusable()[0]?.focus());

    const onKeyDown = (e) => {
      if (e.key === "Escape") {
        onClose();
        return;
      }
      if (e.key !== "Tab") return;
      const focusable = getFocusable();
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last?.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first?.focus();
        }
      }
    };

    document.addEventListener("keydown", onKeyDown);
    return () => {
      cancelAnimationFrame(frame);
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = "";
      previous?.focus();
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div role="presentation">
      {/* Backdrop — decorative only; keyboard users close via Escape or the × button.
          If you want backdrop-click-to-close, use a <button> with aria-hidden="true"
          and tabIndex={-1} so it stays off the focus order. */}
      <div
        aria-hidden="true"
        className="fixed inset-0 z-40 bg-foreground/50 backdrop-blur-sm"
      />

      {/* Centering wrapper — flex avoids translate-fraction positioning.
          items-end anchors to the bottom on mobile; sm:items-center centers on desktop.
          For a true bottom-sheet with directional rounding, override border-radius
          via a CSS custom property at the sm: breakpoint. */}
      <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center sm:p-4">
        <div
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
          aria-labelledby="confirm-title"
          aria-describedby="confirm-desc"
          data-slot="dialog"
          className="relative w-full bg-background shadow-2xl rounded-xl sm:max-w-sm"
        >
          {/* Close × — icon-only, so aria-label is required */}
          <button
            type="button"
            onClick={onClose}
            aria-label="Close dialog"
            className="absolute right-4 top-4 rounded-md p-1 text-muted-foreground transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            <X className="size-4" aria-hidden="true" />
          </button>

          {/* Header */}
          <div className="flex flex-col gap-2 p-6 pb-4">
            <div className="flex items-center gap-3">
              <div className="flex size-10 shrink-0 items-center justify-center rounded-full bg-destructive/10">
                <AlertTriangle className="size-5 text-destructive" aria-hidden="true" />
              </div>
              <h2
                id="confirm-title"
                className="text-base font-semibold leading-tight text-foreground"
              >
                Delete {itemName}?
              </h2>
            </div>
            <p id="confirm-desc" className="text-sm leading-relaxed text-muted-foreground">
              This action is permanent and cannot be undone. All data associated with{" "}
              <strong className="font-medium text-foreground">{itemName}</strong> will
              be removed immediately.
            </p>
          </div>

          {/* Footer — flex-col-reverse puts the primary action first on mobile
              (easier thumb reach on a bottom sheet), then sm:flex-row restores
              the Cancel-left / Confirm-right convention on desktop. */}
          <div className="flex flex-col-reverse gap-2 p-6 pt-2 sm:flex-row sm:justify-end">
            <button
              type="button"
              onClick={onClose}
              className="inline-flex h-9 items-center justify-center rounded-md border border-input bg-background px-4 text-sm font-medium text-foreground shadow-xs transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={onConfirm}
              disabled={isDeleting}
              aria-busy={isDeleting}
              className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-destructive px-4 text-sm font-medium text-primary-foreground transition-colors duration-150 hover:bg-destructive/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
            >
              {isDeleting && <Loader2 className="size-4 animate-spin" aria-hidden="true" />}
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
