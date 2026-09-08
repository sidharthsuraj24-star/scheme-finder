import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Scheme Finder | Kerala",
  description:
    "Simple bilingual helper to find Kerala / India welfare schemes you may be eligible for.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
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
        <div className="mx-auto min-h-screen w-full max-w-lg px-4 pb-10 pt-4 sm:px-6">
          {children}
        </div>
      </body>
    </html>
  );
}
