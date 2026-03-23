import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Jarvis",
  description: "Personal AI Assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
