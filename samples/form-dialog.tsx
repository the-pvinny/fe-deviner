export function InviteDialog({
  open,
  onClose,
  onSuccess,
}: {
  open: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
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
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = "";
      previous?.focus();
    };
  }, [open, onClose]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    const data = new FormData(e.currentTarget);
    const email = data.get("email");

    if (!email) {
      setError("Email address is required.");
      setIsSubmitting(false);
      return;
    }

    // Replace with real API call; call onSuccess() and onClose() on resolve.
    setTimeout(() => {
      setIsSubmitting(false);
      onSuccess?.();
      onClose();
    }, 1200);
  };

  if (!open) return null;

  return (
    <div role="presentation">
      {/* Backdrop — decorative. See confirmation-dialog.tsx for backdrop-click pattern. */}
      <div
        aria-hidden="true"
        className="fixed inset-0 z-40 bg-foreground/50 backdrop-blur-sm"
      />

      <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center sm:p-4">
        <div
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
          aria-labelledby="invite-title"
          aria-describedby="invite-desc"
          data-slot="dialog"
          className="relative w-full bg-background shadow-2xl rounded-xl sm:max-w-md"
        >
          <button
            type="button"
            onClick={onClose}
            aria-label="Close dialog"
            className="absolute right-4 top-4 rounded-md p-1 text-muted-foreground transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            <X className="size-4" aria-hidden="true" />
          </button>

          <form onSubmit={handleSubmit} noValidate>
            {/* Header */}
            <div className="flex flex-col gap-1.5 p-6 pb-0">
              <h2
                id="invite-title"
                className="text-base font-semibold leading-tight text-foreground"
              >
                Invite team member
              </h2>
              <p id="invite-desc" className="text-sm text-muted-foreground">
                They will receive an email invitation to join your workspace.
              </p>
            </div>

            {/* Body */}
            <div className="flex flex-col gap-4 p-6">
              {/* Email — autoFocus moves focus here on open; aria-invalid reflects validation state */}
              <div className="flex flex-col gap-1.5">
                <label
                  htmlFor="invite-email"
                  className="text-sm font-medium text-foreground"
                >
                  Email address
                  <span className="ml-1 text-muted-foreground" aria-hidden="true">*</span>
                </label>
                <input
                  id="invite-email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  autoFocus
                  required
                  aria-required="true"
                  aria-invalid={error ? "true" : "false"}
                  aria-describedby={error ? "invite-email-error" : undefined}
                  placeholder="colleague@example.com"
                  className="h-9 w-full rounded-md border border-input bg-background px-3 text-sm text-foreground transition-colors duration-150 placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                />
                {error && (
                  <p id="invite-email-error" role="alert" className="text-xs text-destructive">
                    {error}
                  </p>
                )}
              </div>

              {/* Role */}
              <div className="flex flex-col gap-1.5">
                <label
                  htmlFor="invite-role"
                  className="text-sm font-medium text-foreground"
                >
                  Role
                </label>
                <select
                  id="invite-role"
                  name="role"
                  defaultValue="member"
                  className="h-9 w-full rounded-md border border-input bg-background px-3 text-sm text-foreground transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <option value="member">Member — can view and comment</option>
                  <option value="editor">Editor — can edit content</option>
                  <option value="admin">Admin — full access</option>
                </select>
              </div>
            </div>

            {/* Footer */}
            <div className="flex flex-col-reverse gap-2 p-6 pt-0 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={onClose}
                className="inline-flex h-9 items-center justify-center rounded-md border border-input bg-background px-4 text-sm font-medium text-foreground shadow-xs transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                aria-busy={isSubmitting}
                className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground transition-colors duration-150 hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
              >
                {isSubmitting && <Loader2 className="size-4 animate-spin" aria-hidden="true" />}
                Send invite
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
