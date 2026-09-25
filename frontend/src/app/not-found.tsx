import Link from "next/link";

export default function NotFound() {
  return (
    <main id="main-content" tabIndex={-1} className="space-y-4 py-8">
      <h1 className="text-2xl font-extrabold text-brand-900">Page not found</h1>
      <p className="text-base text-slate-700">
        This page does not exist. Go back to Scheme Finder to start a search.
      </p>
      <p>
        <Link
          href="/"
          className="inline-flex min-h-tap items-center rounded-xl bg-brand-700 px-4 py-3 font-bold text-white"
        >
          Go to Scheme Finder
        </Link>
      </p>
    </main>
  );
}
