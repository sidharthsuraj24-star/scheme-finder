import type { Metadata, Viewport } from "next";
import SkipLink from "@/components/SkipLink";
import "./globals.css";

export const metadata: Metadata = {
  title: "Scheme Finder",
  description:
    "Simple trilingual (English / हिंदी / മലയാളം) helper to find welfare schemes you may be eligible for — India + selected other countries.",
};

// WCAG 1.4.4 / 1.4.10: never block pinch-zoom (no maximum-scale / user-scalable=no).
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#15803d",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">
        <SkipLink />
        <div className="mx-auto min-h-screen w-full max-w-lg px-4 pb-10 pt-4 sm:px-6">
          {children}
        </div>
      </body>
    </html>
  );
}
