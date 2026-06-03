export function MainNavigation({
  siteName,
  links,
  activeHref,
}: {
  siteName: string;
  links: { href: string; label: string }[];
  activeHref: string;
}) {
  return (
    <header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur-sm">
      <nav
        aria-label="Main navigation"
        className="mx-auto flex h-16 max-w-screen-xl items-center px-4 sm:px-6 lg:px-8"
      >
        <a
          href="/"
          aria-label="Home"
          className="flex shrink-0 items-center gap-2 rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          <span className="text-sm font-semibold">{siteName}</span>
        </a>

        <ul role="list" className="ml-8 hidden items-center gap-1 md:flex">
          {links.map((link) => {
            const isActive = link.href === activeHref;
            return (
              <li key={link.href}>
                <a
                  href={link.href}
                  aria-current={isActive ? "page" : undefined}
                  className={
                    isActive
                      ? "rounded-md bg-accent px-3 py-1.5 text-sm font-medium text-accent-foreground transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                      : "rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  }
                >
                  {link.label}
                </a>
              </li>
            );
          })}
        </ul>

        <div className="ml-auto flex items-center gap-2">
          <a
            href="/sign-in"
            className="hidden rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors duration-150 hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 md:inline-flex"
          >
            Sign in
          </a>
          <a
            href="/get-started"
            className="hidden rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground transition-colors duration-150 hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 md:inline-flex"
          >
            Get started
          </a>
          <button
            type="button"
            aria-label="Open menu"
            aria-expanded={false}
            aria-controls="mobile-menu"
            className="flex size-9 items-center justify-center rounded-md transition-colors duration-150 hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 md:hidden"
          >
            <span className="sr-only">Menu</span>
          </button>
        </div>
      </nav>
    </header>
  );
}
