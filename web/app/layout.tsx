import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-poppins",
});

export const metadata: Metadata = {
  title: "Coding Trainer AI - Master's Figma Studio",
  description: "Figma-inspired Dark Canvas UI for Master's AI & Robotics Training",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={poppins.variable}>
      <body className="font-poppins bg-[#1e1e1e] text-white antialiased">
        {children}
      </body>
    </html>
  );
}
