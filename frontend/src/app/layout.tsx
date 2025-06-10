import { ThemeProvider } from "@/components/theme-provider";
import { TRPCProvider } from "@/components/providers/trpc-provider";
import { ClientSessionProvider } from "@/components/providers/session-provider";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import type * as React from "react";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SEO Agent",
  description: "AI-powered SEO automation tool",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ClientSessionProvider>
          <TRPCProvider>
            <ThemeProvider
              attribute="class"
              defaultTheme="system"
              enableSystem
              disableTransitionOnChange
            >
              {children}
            </ThemeProvider>
          </TRPCProvider>
        </ClientSessionProvider>
      </body>
    </html>
  );
}
