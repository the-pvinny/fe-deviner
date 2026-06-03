export function MinimalFooter({
  siteName,
  links,
}: {
  siteName: string;
  links: { href: string; label: string }[];
}) {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-background">
      {/* Single-row layout — collapses to a stacked column on mobile.
          Copyright uses `order-last sm:order-none` so the brand stays first on
          mobile (most prominent), while the desktop order is brand → © → links. */}
      <div className="mx-auto flex max-w-screen-xl flex-col items-center justify-between gap-4 px-4 py-8 sm:flex-row sm:px-6 lg:px-8">
        <a
          href="/"
          aria-label="Home"
          className="inline-flex items-center gap-2 rounded-sm text-sm font-semibold text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          {siteName}
        </a>

        <p className="order-last text-xs text-muted-foreground sm:order-none">
          © {year} {siteName}
        </p>

        <nav aria-label="Footer">
          <ul role="list" className="flex items-center gap-4 sm:gap-6">
            {links.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  className="rounded-sm text-xs text-muted-foreground transition-colors duration-150 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </footer>
  );
}
