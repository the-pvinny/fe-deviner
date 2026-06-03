export function FullBleedHero({
  backgroundSrc,
  headline,
  subheadline,
  primaryLabel,
  secondaryLabel,
}: {
  backgroundSrc: string;
  headline: string;
  subheadline: string;
  primaryLabel: string;
  secondaryLabel: string;
}) {
  return (
    <section
      aria-labelledby="hero-heading"
      className="relative flex min-h-svh items-center justify-center overflow-hidden"
    >
      <div className="absolute inset-0 -z-10">
        <img
          src={backgroundSrc}
          alt=""
          aria-hidden="true"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-foreground/50" aria-hidden="true" />
      </div>

      <div className="relative mx-auto max-w-4xl px-4 py-24 text-center">
        <h1
          id="hero-heading"
          className="text-5xl font-bold tracking-tight text-primary-foreground sm:text-6xl lg:text-7xl"
        >
          {headline}
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-xl leading-relaxed text-primary-foreground/80">
          {subheadline}
        </p>
        <div className="mt-10 flex flex-col justify-center gap-3 sm:flex-row">
          <button
            type="button"
            className="inline-flex h-10 items-center justify-center rounded-md bg-primary-foreground px-6 text-base font-medium text-foreground transition-colors duration-150 hover:bg-primary-foreground/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            {primaryLabel}
          </button>
          <button
            type="button"
            className="inline-flex h-10 items-center justify-center rounded-md border border-primary-foreground px-6 text-base font-medium text-primary-foreground transition-colors duration-150 hover:bg-primary-foreground/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            {secondaryLabel}
          </button>
        </div>
      </div>
    </section>
  );
}
