import NextAuth, { type DefaultSession } from "next-auth";
import Google from "next-auth/providers/google";
import { DrizzleAdapter } from "@auth/drizzle-adapter";
import { db } from "./db";
import { eq } from "drizzle-orm";
import { users } from "./db/schema/auth";

declare module "next-auth" {
  interface Session extends DefaultSession {
    user: {
      id: string;
    } & DefaultSession["user"];
  }
}

const authConfig = {
  callbacks: {
    session({ session, user }: any) {
      if (session.user) {
        session.user.id = user.id;
      }
      return session;
    },
    redirect({ url, baseUrl }: any) {
      if (url.startsWith(baseUrl)) {
        return `${baseUrl}/content-optimizer`;
      }
      return url;
    },
  },
  events: {
    async createUser({ user }: any) {
      if (!user.email || !user.id) return;

      await db.update(users).set({
        planType: "FREE",
        monthlyCredits: 50,
        usedCredits: 0
      }).where(eq(users.id, user.id));
    },
  },
  adapter: DrizzleAdapter(db),
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID || "dummy-client-id",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "dummy-client-secret",
    })
  ],
};

export const {
  handlers: { GET, POST },
  signIn,
  signOut,
  auth,
} = NextAuth(authConfig);
