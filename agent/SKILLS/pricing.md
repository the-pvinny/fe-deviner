# SKILL — Pricing

Applies within CONFIG.md and METHOD.md constraints. Works alongside any STYLES/ or PATTERNS/ file.

---

## Core Principle

Pricing tables are decision architecture. Every visual choice either helps users self-select into the right plan or creates friction that delays or prevents conversion. The goal is not to make every plan look attractive — it is to make the _right_ plan immediately obvious for each visitor type. Highlight the recommended plan. Make the value difference clear. Remove cognitive load.

---

## Anatomy

| Slot | Content | Required |
|---|---|---|
| Plan name | Short, memorable name ("Starter", "Pro", "Enterprise") | Yes |
| Price | The number — prominent, unambiguous | Yes |
| Billing period | "/month" or "/year" — small, adjacent to price | Yes |
| Description | One-sentence positioning statement | Yes |
| CTA | One action per plan | Yes |
| Feature list | Specific, scannable, ordered by importance | Yes |
| Highlighted plan | Visual treatment to distinguish recommended | Contextual |
| Annual toggle | Switch between monthly/annual pricing | Common |

---

## Standard Three-Column Layout

```tsx
<section aria-labelledby="pricing-heading" className="py-16 lg:py-24">
  <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="text-center mb-12">
      <h2 id="pricing-heading" className="text-3xl lg:text-4xl font-bold tracking-tight mb-4">
        Simple, transparent pricing
      </h2>
      <p className="text-lg text-muted-foreground max-w-xl mx-auto">
        Choose the plan that fits your needs. Upgrade or downgrade at any time.
      </p>
      <BillingToggle value={billing} onChange={setBilling} />
    </div>

    <div
      className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 items-stretch"
      role="list"
      aria-label="Pricing plans"
    >
      {plans.map((plan) => (
        <PricingCard key={plan.id} plan={plan} billing={billing} />
      ))}
    </div>

    <p className="text-center text-xs text-muted-foreground mt-8">
      All plans include a 14-day free trial. No credit card required.
    </p>
  </div>
</section>
```

---

## Pricing Card Component

```tsx
function PricingCard({ plan, billing }) {
  const isHighlighted = plan.highlighted
  const price = billing === "annual" ? plan.annualPrice : plan.monthlyPrice
  const savings = billing === "annual" && plan.annualSavings

  return (
    <div
      role="listitem"
      aria-label={`${plan.name} plan`}
      className={cn(
        "relative flex flex-col rounded-xl border p-6 lg:p-8",
        "transition-shadow duration-200",
        isHighlighted
          ? "border-primary bg-primary text-primary-foreground shadow-xl scale-[1.02] lg:scale-105"
          : "border-border bg-card shadow-sm hover:shadow-md"
      )}
    >
      {/* Recommended badge */}
      {plan.badge && (
        <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
          <span className={cn(
            "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold",
            isHighlighted
              ? "bg-background text-foreground"
              : "bg-primary text-primary-foreground"
          )}>
            {plan.badge}
          </span>
        </div>
      )}

      {/* Plan name and description */}
      <div className="mb-6">
        <h3 className={cn(
          "text-base font-semibold mb-1",
          isHighlighted ? "text-primary-foreground" : "text-foreground"
        )}>
          {plan.name}
        </h3>
        <p className={cn(
          "text-sm",
          isHighlighted ? "text-primary-foreground/80" : "text-muted-foreground"
        )}>
          {plan.description}
        </p>
      </div>

      {/* Price */}
      <div className="mb-6">
        <div className="flex items-baseline gap-1">
          {price === "Custom" ? (
            <span className="text-3xl font-bold">Custom</span>
          ) : (
            <>
              <span className={cn(
                "text-sm font-medium",
                isHighlighted ? "text-primary-foreground/80" : "text-muted-foreground"
              )}>$</span>
              <span className="text-4xl font-bold tabular-nums">{price}</span>
              <span className={cn(
                "text-sm",
                isHighlighted ? "text-primary-foreground/70" : "text-muted-foreground"
              )}>
                /mo
              </span>
            </>
          )}
        </div>
        {savings && (
          <p className={cn(
            "text-xs mt-1",
            isHighlighted ? "text-primary-foreground/70" : "text-success"
          )}>
            Save {savings}% with annual billing
          </p>
        )}
        {billing === "annual" && price !== "Custom" && (
          <p className={cn(
            "text-xs",
            isHighlighted ? "text-primary-foreground/60" : "text-muted-foreground"
          )}>
            Billed annually (${price * 12}/yr)
          </p>
        )}
      </div>

      {/* CTA */}
      <Button
        asChild
        size="lg"
        variant={isHighlighted ? "secondary" : "default"}
        className="w-full mb-8"
      >
        <a href={plan.ctaHref}>{plan.ctaLabel}</a>
      </Button>

      {/* Features */}
      <div className="flex-1">
        {plan.featureGroupLabel && (
          <p className={cn(
            "text-xs font-semibold uppercase tracking-wider mb-3",
            isHighlighted ? "text-primary-foreground/70" : "text-muted-foreground"
          )}>
            {plan.featureGroupLabel}
          </p>
        )}
        <ul role="list" className="flex flex-col gap-2.5">
          {plan.features.map((feature) => (
            <li key={feature.label} className="flex items-start gap-2.5 text-sm">
              {feature.included ? (
                <Check
                  className={cn(
                    "size-4 mt-0.5 shrink-0",
                    isHighlighted ? "text-primary-foreground" : "text-success"
                  )}
                  aria-hidden="true"
                />
              ) : (
                <Minus
                  className="size-4 mt-0.5 shrink-0 text-muted-foreground"
                  aria-hidden="true"
                />
              )}
              <span className={cn(
                feature.included
                  ? (isHighlighted ? "text-primary-foreground" : "text-foreground")
                  : "text-muted-foreground line-through"
              )}>
                {feature.label}
                {feature.tooltip && (
                  <button
                    type="button"
                    aria-label={`More about ${feature.label}`}
                    className="ml-1 align-middle opacity-60 hover:opacity-100"
                  >
                    <HelpCircle className="inline size-3" aria-hidden="true" />
                  </button>
                )}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
```

---

## Billing Toggle

```tsx
function BillingToggle({ value, onChange }) {
  return (
    <div className="mt-8 flex items-center justify-center gap-3">
      <span className={cn(
        "text-sm",
        value === "monthly" ? "text-foreground font-medium" : "text-muted-foreground"
      )}>
        Monthly
      </span>
      <button
        type="button"
        role="switch"
        aria-checked={value === "annual"}
        aria-label="Toggle annual billing"
        onClick={() => onChange(value === "monthly" ? "annual" : "monthly")}
        className={cn(
          "relative inline-flex h-6 w-11 shrink-0 items-center rounded-full",
          "transition-colors duration-200 ease-in-out",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
          value === "annual" ? "bg-primary" : "bg-input"
        )}
      >
        <span
          aria-hidden="true"
          className={cn(
            "pointer-events-none block size-4 rounded-full bg-white shadow-sm",
            "transition-transform duration-200 ease-in-out",
            value === "annual" ? "translate-x-6" : "translate-x-1"
          )}
        />
      </button>
      <span className={cn(
        "text-sm",
        value === "annual" ? "text-foreground font-medium" : "text-muted-foreground"
      )}>
        Annual
        <span className="ml-1.5 inline-flex items-center rounded-full bg-success/10 px-1.5 py-0.5 text-xs font-medium text-success">
          Save 20%
        </span>
      </span>
    </div>
  )
}
```

`role="switch"` + `aria-checked` is the correct ARIA pattern for a toggle. Do not use `role="checkbox"`.

---

## Enterprise / Custom Tier

Enterprise rows break the card grid — use a horizontal band below the card columns.

```tsx
<div className="mt-6 rounded-xl border border-border bg-muted/30 p-6 lg:p-8">
  <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
    <div>
      <h3 className="text-base font-semibold text-foreground mb-1">Enterprise</h3>
      <p className="text-sm text-muted-foreground max-w-lg">
        Custom contracts, SLA guarantees, SSO, dedicated support, and volume pricing.
        Contact us to build a plan for your organization.
      </p>
    </div>
    <div className="flex items-center gap-3 shrink-0">
      <Button variant="outline" asChild>
        <a href="/contact">Talk to sales</a>
      </Button>
      <Button asChild>
        <a href="/enterprise">Learn more</a>
      </Button>
    </div>
  </div>
</div>
```

---

## Feature Comparison Table

For 4+ plans or when feature differences are complex, supplement the cards with a full table.

```tsx
<section aria-labelledby="comparison-heading" className="mt-16">
  <h2 id="comparison-heading" className="sr-only">Plan feature comparison</h2>
  <div className="overflow-x-auto">
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr className="border-b border-border">
          <th scope="col" className="text-left py-3 pr-6 font-semibold text-foreground w-1/2">
            Feature
          </th>
          {plans.map((plan) => (
            <th
              key={plan.id}
              scope="col"
              className={cn(
                "py-3 px-4 text-center font-semibold",
                plan.highlighted ? "text-primary" : "text-foreground"
              )}
            >
              {plan.name}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {featureGroups.map((group) => (
          <>
            <tr key={`group-${group.label}`} className="border-b border-border">
              <td colSpan={plans.length + 1} className="py-3 pr-6 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {group.label}
              </td>
            </tr>
            {group.features.map((feature) => (
              <tr key={feature.id} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors duration-100">
                <td className="py-3 pr-6 text-foreground">
                  {feature.label}
                </td>
                {plans.map((plan) => {
                  const value = feature.values[plan.id]
                  return (
                    <td key={plan.id} className="py-3 px-4 text-center">
                      {typeof value === "boolean" ? (
                        value
                          ? <Check className="size-4 text-success mx-auto" aria-label="Included" />
                          : <Minus className="size-4 text-muted-foreground mx-auto" aria-label="Not included" />
                      ) : (
                        <span className="text-foreground">{value}</span>
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </>
        ))}
      </tbody>
    </table>
  </div>
</section>
```

---

## Visual Hierarchy of the Highlighted Plan

Three correct approaches, ordered by visual strength:

1. **Elevated + inverted color** — recommended plan uses `bg-primary text-primary-foreground` and `scale-105`. Strongest signal.
2. **Border accent** — `border-2 border-primary` with a "Most popular" badge. Lighter treatment for minimal/editorial styles.
3. **Background tint** — `bg-primary/5` with an accent badge. Subtlest option.

Never highlight more than one plan. If everything is recommended, nothing is.

---

## Responsive Behavior

| Breakpoint | Layout |
|---|---|
| Mobile | Single-column stacked cards |
| md (768px) | Three columns (standard 3-plan layout) |
| lg (1024px) | Highlighted plan scales slightly (`scale-105`) |

On mobile, the highlighted plan loses its `scale-105` treatment — stacking prevents the layout offset from working. The inverted color and badge are sufficient at mobile scale.

Feature comparison table: scroll horizontally on mobile. Wrap in `overflow-x-auto`. Never truncate or hide columns — the comparison is the value.

---

## Accessibility

- Pricing section: `<section aria-labelledby>` pointing to the heading
- Card grid: `role="list"` + individual `role="listitem"` on each card — allows screen readers to announce card count
- Each card: `aria-label="{plan.name} plan"` for card landmark context
- Billing toggle: `role="switch"` + `aria-checked` — standard ARIA switch pattern
- Feature check/minus icons: `aria-label="Included"` / `aria-label="Not included"` — visual icons need text equivalents
- Comparison table: proper `<thead>`, `<th scope="col">` for plan names, `<th scope="row">` for feature names if applicable
- "Custom" or "Contact us" pricing: announce as such — don't leave an empty price cell

---

## Common Pitfalls

- **Highlighting every plan:** pricing tables where all three plans have accent borders or "Best value" badges. Pick one.
- **Vague feature names:** "Advanced analytics" vs "Analytics dashboard with 90-day history and CSV export" — the latter removes "what does this actually mean?" friction.
- **Price without period:** "$49" with no "/month" is ambiguous. Always include billing period adjacent to price.
- **No FAQ below pricing:** "What happens when I exceed limits?", "Can I change plans?", "Do you offer refunds?" — these are the objections that stop conversions. Address them directly.
- **Missing comparison table for complex plans:** three cards with 15 features each become a wall. A comparison table is more scannable.
- **Annual savings hidden in fine print:** if annual billing saves 20%, that should be in the toggle label, not buried in the card.
