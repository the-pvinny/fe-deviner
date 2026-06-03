export function SiteFooter({
  siteName,
  tagline,
  columns,
  legalLinks,
  socialLinks,
}: {
  siteName: string;
  tagline: string;
  columns: { label: string; links: { href: string; label: string }[] }[];
  legalLinks: { href: string; label: string }[];
  socialLinks?: { platform: string; href: string }[];
}) {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-background">
      {/* Main grid — brand column spans 2 at lg so the link columns get even width */}
      <div className="mx-auto max-w-screen-xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-5">
          {/* Brand */}
          <div className="col-span-2 sm:col-span-3 lg:col-span-2">
            <a
              href="/"
              aria-label="Home"
              className="inline-flex w-fit items-center gap-2 rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            >
              <span className="text-sm font-semibold text-foreground">{siteName}</span>
            </a>
            <p className="mt-4 max-w-xs text-sm leading-relaxed text-muted-foreground">
              {tagline}
            </p>

            {socialLinks && socialLinks.length > 0 && (
              <ul role="list" className="mt-6 flex flex-wrap items-center gap-4">
                {socialLinks.map((link) => (
                  <li key={link.platform}>
                    <a
                      href={link.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="rounded-sm text-sm text-muted-foreground transition-colors duration-150 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    >
                      {link.platform}
                      <span className="sr-only"> (opens in new tab)</span>
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Link columns — each column is a labelled <nav> so screen readers can
              skip between them. The visible <h3> doubles as the column heading
              and the aria-labelledby target for its <nav>. */}
          {columns.map((column, index) => {
            const headingId = "footer-col-" + index;
            return (
              <nav key={column.label} aria-labelledby={headingId}>
                <h3
                  id={headingId}
                  className="mb-4 text-xs font-semibold uppercase tracking-wider text-foreground"
                >
                  {column.label}
                </h3>
                <ul role="list" className="flex flex-col gap-3">
                  {column.links.map((link) => (
                    <li key={link.href}>
                      <a
                        href={link.href}
                        className="rounded-sm text-sm text-muted-foreground transition-colors duration-150 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                      >
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </nav>
            );
          })}
        </div>
      </div>

      {/* Bottom bar — copyright + legal nav.
          Year is generated dynamically so it never goes stale. */}
      <div className="border-t border-border">
        <div className="mx-auto flex max-w-screen-xl flex-col items-center justify-between gap-4 px-4 py-6 sm:flex-row sm:px-6 lg:px-8">
          <p className="text-xs text-muted-foreground">
            © {year} {siteName}. All rights reserved.
          </p>
          <nav aria-label="Legal">
            <ul role="list" className="flex items-center gap-4 sm:gap-6">
              {legalLinks.map((link) => (
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
      </div>
    </footer>
  );
}
