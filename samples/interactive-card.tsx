import type { ReactNode } from "react";

export function InteractiveCard({
  href,
  title,
  children,
}: {
  href: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <a
      href={href}
      className="group block rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
    >
      <div
        data-slot="card"
        className="rounded-lg border bg-card text-card-foreground shadow-sm transition-all duration-200 group-hover:-translate-y-0.5 group-hover:shadow-md group-focus-visible:ring-2 group-focus-visible:ring-ring"
      >
        <div data-slot="card-header" className="flex flex-col gap-1.5 p-6">
          <h3 className="text-base font-semibold leading-tight">{title}</h3>
        </div>
        <div data-slot="card-content" className="p-6 pt-0">
          {children}
        </div>
      </div>
    </a>
  );
}
