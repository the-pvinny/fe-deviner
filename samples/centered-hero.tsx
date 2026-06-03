export function CenteredHero({
  eyebrow,
  headline,
  subheadline,
  primaryHref,
  primaryLabel,
  secondaryHref,
  secondaryLabel,
  trustSignal,
}: {
  eyebrow?: string;
  headline: string;
  subheadline: string;
  primaryHref: string;
  primaryLabel: string;
  secondaryHref?: string;
  secondaryLabel?: string;
  trustSignal?: string;
}) {
  return (
    <section
      aria-labelledby="hero-heading"
      className="relative flex flex-col items-center justify-center px-4 pt-24 pb-20 text-center sm:pt-32 sm:pb-28"
    >
      {eyebrow ? (
        <span className="mb-6 inline-flex items-center gap-1.5 rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-muted-foreground">
          {eyebrow}
        </span>
      ) : null}

      <h1
        id="hero-heading"
        className="max-w-3xl text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl"
      >
        {headline}
      </h1>

      <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground sm:text-xl">
        {subheadline}
      </p>

      <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row">
        <a
          href={primaryHref}
          className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-6 text-base font-medium text-primary-foreground transition-colors duration-150 hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          {primaryLabel}
        </a>
        {secondaryLabel && secondaryHref ? (
          <a
            href={secondaryHref}
            className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-6 text-base font-medium text-foreground shadow-xs transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            {secondaryLabel}
          </a>
        ) : null}
      </div>

      {trustSignal ? (
        <p className="mt-6 text-xs text-muted-foreground">{trustSignal}</p>
      ) : null}
    </section>
  );
}
