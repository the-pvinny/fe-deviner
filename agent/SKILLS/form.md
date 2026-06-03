# SKILL — Form

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

Forms are conversations. Every field is a question. Users answer them to accomplish a goal — submitting is the reward for completing the exchange. Good forms minimize friction, surface errors before submission when possible, and never leave the user confused about what is needed or what went wrong.

---

## Field Anatomy — Compound Structure

Every field is a compound of four parts: label, input, description, and error. All four live together.

```tsx
function FormField({ id, label, description, error, required, children }) {
  return (
    <div data-slot="field" className="flex flex-col gap-1.5">
      <label
        htmlFor={id}
        className={cn(
          "text-sm font-medium leading-none",
          error && "text-destructive"
        )}
      >
        {label}
        {required && <span className="text-destructive ml-0.5" aria-hidden="true">*</span>}
      </label>
      {children}
      {description && !error && (
        <p id={`${id}-description`} className="text-xs text-muted-foreground">
          {description}
        </p>
      )}
      {error && (
        <p id={`${id}-error`} role="alert" className="text-xs text-destructive flex items-center gap-1">
          <AlertCircle className="size-3 shrink-0" aria-hidden="true" />
          {error}
        </p>
      )}
    </div>
  )
}
```

**Rule:** Never show description and error simultaneously — the error replaces the description.

---

## Input Styles

### Text input

```tsx
<input
  id={id}
  type="text"
  aria-describedby={error ? `${id}-error` : description ? `${id}-description` : undefined}
  aria-invalid={!!error}
  className={cn(
    "flex h-9 w-full rounded-md border border-input bg-background px-3 py-1",
    "text-sm shadow-xs placeholder:text-muted-foreground",
    "transition-colors duration-150",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
    "disabled:cursor-not-allowed disabled:opacity-50",
    error && "border-destructive focus-visible:ring-destructive"
  )}
/>
```

### Textarea

```tsx
<textarea
  id={id}
  rows={4}
  aria-describedby={error ? `${id}-error` : undefined}
  aria-invalid={!!error}
  className={cn(
    "flex w-full rounded-md border border-input bg-background px-3 py-2",
    "text-sm shadow-xs placeholder:text-muted-foreground resize-y min-h-20",
    "transition-colors duration-150",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
    "disabled:cursor-not-allowed disabled:opacity-50",
    error && "border-destructive focus-visible:ring-destructive"
  )}
/>
```

### Select

```tsx
<select
  id={id}
  aria-describedby={error ? `${id}-error` : undefined}
  aria-invalid={!!error}
  className={cn(
    "flex h-9 w-full rounded-md border border-input bg-background px-3 py-1",
    "text-sm shadow-xs",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
    "disabled:cursor-not-allowed disabled:opacity-50"
  )}
>
  <option value="">Select an option</option>
  {options.map((opt) => (
    <option key={opt.value} value={opt.value}>{opt.label}</option>
  ))}
</select>
```

### Checkbox

```tsx
<div className="flex items-center gap-2">
  <input
    type="checkbox"
    id={id}
    className={cn(
      "size-4 rounded border-input accent-primary",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
    )}
  />
  <label htmlFor={id} className="text-sm leading-none">{label}</label>
</div>
```

### Radio group

```tsx
<fieldset>
  <legend className="text-sm font-medium mb-2">{groupLabel}</legend>
  <div className="flex flex-col gap-2">
    {options.map((opt) => (
      <div key={opt.value} className="flex items-center gap-2">
        <input
          type="radio"
          id={`${name}-${opt.value}`}
          name={name}
          value={opt.value}
          className="size-4 accent-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        />
        <label htmlFor={`${name}-${opt.value}`} className="text-sm">{opt.label}</label>
      </div>
    ))}
  </div>
</fieldset>
```

**Rule:** Radio groups always use `<fieldset>` + `<legend>`. Never style them as a card grid with `<div onClick>`.

---

## Form Layout

### Single-column (default, mobile-first)

```tsx
<form onSubmit={onSubmit} noValidate className="flex flex-col gap-6" aria-label="Form title">
  <FormField id="name" label="Name" required error={errors.name}>
    <input id="name" type="text" ... />
  </FormField>
  <FormField id="email" label="Email address" required error={errors.email}>
    <input id="email" type="email" ... />
  </FormField>
  <div className="flex gap-3 pt-2">
    <Button type="submit" disabled={isSubmitting} aria-busy={isSubmitting}>
      {isSubmitting && <Loader2 className="size-4 animate-spin" aria-hidden="true" />}
      Submit
    </Button>
    <Button type="button" variant="outline" onClick={onCancel}>Cancel</Button>
  </div>
</form>
```

### Two-column at `md:`

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6">
  <FormField id="first-name" label="First name" ...>...</FormField>
  <FormField id="last-name" label="Last name" ...>...</FormField>
</div>
```

Keep single-column for: sensitive fields (passwords, payment), fields with long descriptions, mobile-primary forms. Two-column for: registration forms, settings, dense data entry on desktop.

---

## Validation States

### Field-level inline error (preferred)

Show the error inline as soon as the field loses focus (on blur), not only on submit. This reduces "wall of errors" on submission.

```tsx
const [touched, setTouched] = useState(false)
const error = touched && !value ? "This field is required" : undefined

<FormField id="email" label="Email" error={error}>
  <input
    id="email"
    type="email"
    onBlur={() => setTouched(true)}
    aria-invalid={!!error}
    aria-describedby={error ? "email-error" : undefined}
  />
</FormField>
```

### Form-level error summary

When multiple validation errors exist after submission, render a summary at the top of the form and move focus to it:

```tsx
{submitErrors.length > 0 && (
  <div
    role="alert"
    aria-live="assertive"
    tabIndex={-1}
    ref={errorSummaryRef}
    className="rounded-md border border-destructive bg-destructive/10 p-4"
  >
    <p className="text-sm font-medium text-destructive mb-2">
      Please fix the following errors:
    </p>
    <ul className="text-sm text-destructive list-disc list-inside space-y-1">
      {submitErrors.map((err) => (
        <li key={err.field}>
          <a href={`#${err.field}`} className="hover:underline">{err.message}</a>
        </li>
      ))}
    </ul>
  </div>
)}
```

Move focus to `errorSummaryRef.current?.focus()` after failed submission.

### Success state

```tsx
{isSuccess && (
  <div role="status" className="rounded-md border border-border bg-success/10 p-4 flex items-start gap-3">
    <CheckCircle className="size-4 text-success shrink-0 mt-0.5" aria-hidden="true" />
    <p className="text-sm text-success-foreground">{successMessage}</p>
  </div>
)}
```

---

## Multi-Step Forms

Use a stepped layout when a form has more than 6–8 fields or when fields belong to distinct categories (personal → payment → confirmation).

### Step indicator

```tsx
<nav aria-label="Form progress">
  <ol className="flex items-center gap-2">
    {steps.map((step, i) => (
      <li key={step.id} className="flex items-center gap-2">
        <div
          aria-current={i === currentStep ? "step" : undefined}
          className={cn(
            "flex size-7 items-center justify-center rounded-full text-xs font-semibold",
            i < currentStep && "bg-primary text-primary-foreground",
            i === currentStep && "bg-primary text-primary-foreground ring-2 ring-primary ring-offset-2",
            i > currentStep && "bg-muted text-muted-foreground"
          )}
        >
          {i < currentStep ? <Check className="size-3.5" aria-hidden="true" /> : i + 1}
        </div>
        <span className={cn(
          "text-sm hidden sm:block",
          i === currentStep ? "font-medium text-foreground" : "text-muted-foreground"
        )}>
          {step.label}
        </span>
        {i < steps.length - 1 && <div className="h-px w-8 bg-border" aria-hidden="true" />}
      </li>
    ))}
  </ol>
</nav>
```

### Step navigation

- "Back" button: `variant="outline"`, left of "Next"
- "Next" button: `variant="default"`, validates current step before advancing
- "Submit" button: only on final step, replaces "Next"
- Never skip validation on intermediate steps

---

## Password Field

```tsx
function PasswordField({ id, label, ...fieldProps }) {
  const [show, setShow] = useState(false)
  return (
    <FormField id={id} label={label} {...fieldProps}>
      <div className="relative">
        <input
          id={id}
          type={show ? "text" : "password"}
          className={cn(inputBaseClasses, "pr-10")}
          autoComplete="current-password"
        />
        <button
          type="button"
          onClick={() => setShow(!show)}
          aria-label={show ? "Hide password" : "Show password"}
          className="absolute inset-y-0 right-0 flex items-center px-3 text-muted-foreground hover:text-foreground transition-colors duration-150"
        >
          {show ? <EyeOff className="size-4" aria-hidden="true" /> : <Eye className="size-4" aria-hidden="true" />}
        </button>
      </div>
    </FormField>
  )
}
```

---

## Accessibility

- `<form>` must have an accessible name: `aria-label` or `aria-labelledby` pointing to a visible heading
- Every input has a visible `<label>` — never use `placeholder` as a substitute for `<label>`
- `required` fields: mark visually (asterisk) and with `required` HTML attribute; announce to screen readers via `aria-required="true"` if not using native `required`
- `aria-invalid="true"` on inputs with errors; paired with `aria-describedby` pointing to the error message element
- `aria-busy="true"` on the submit button while submitting
- After successful submission of a modal form, return focus to the trigger element
- `autocomplete` attributes on relevant inputs: `"name"`, `"email"`, `"current-password"`, `"new-password"`, `"tel"`, `"street-address"` — improves UX and mobile keyboard behavior

---

## Responsive Behavior

- Single-column on mobile always — never two-column below `md:`
- Submit button: full-width on mobile (`w-full sm:w-auto`), or full-width always for primary forms
- Multi-step step indicator: collapse label text on small screens, show only step numbers
- Consider bottom-sheet pattern on mobile for forms triggered by a button

---

## Common Pitfalls

- **Placeholder as label:** placeholder disappears on focus — users forget what they were filling in. Always use visible labels.
- **Submit on Enter without thought:** `<form>` submits on Enter by default — verify the default behavior is correct, especially in multi-step flows.
- **Missing `noValidate`:** Browser native validation is inconsistent across browsers. Use `noValidate` on `<form>` and handle validation yourself.
- **Error messages that blame:** "Invalid input" is useless. "Email must include @" is actionable.
- **Focus not managed after error:** after a failed submit, focus must be explicitly moved to the first error or the error summary. The user cannot find the error if focus stays on the submit button.
- **Checkbox/radio without fieldset:** grouped radios or a "Terms and conditions" checkbox area without `<fieldset>` + `<legend>` loses grouping context for screen reader users.
