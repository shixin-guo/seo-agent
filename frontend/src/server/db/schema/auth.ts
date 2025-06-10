import { sqliteTable, text, integer, primaryKey } from 'drizzle-orm/sqlite-core';
import { relations, sql } from 'drizzle-orm';
import type { AdapterAccount } from "next-auth/adapters"

export const users = sqliteTable('user', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  name: text('name'),
  email: text('email').unique(),
  emailVerified: integer('emailVerified', { mode: 'timestamp_ms' }),
  image: text('image'),
  usedCredits: integer('usedCredits').default(0),
  
  planType: text('planType').default('FREE'),
  storageUsed: integer('storageUsed').default(0),
  storageLimit: integer('storageLimit').default(104857600),
  monthlyCredits: integer('monthlyCredits').default(50),
  lastCreditReset: integer('lastCreditReset', { mode: 'timestamp_ms' }),
  planStartDate: integer('planStartDate', { mode: 'timestamp_ms' }),
  planEndDate: integer('planEndDate', { mode: 'timestamp_ms' }),
  
  stripeCustomerId: text('stripeCustomerId').unique(),
  stripeSubscriptionId: text('stripeSubscriptionId'),
  subscriptionStatus: text('subscriptionStatus', { length: 20 }),
  
  createdAt: integer("createdAt", { mode: "timestamp_ms" }).default(sql`(strftime('%s','now') * 1000)`),
  updatedAt: integer("updatedAt", { mode: "timestamp_ms" }).default(sql`(strftime('%s','now') * 1000)`),
});

export const accounts = sqliteTable(
  "account",
  {
    userId: text("userId")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    type: text("type").notNull(),
    provider: text("provider").notNull(),
    providerAccountId: text("providerAccountId").notNull(),
    refresh_token: text("refresh_token"),
    access_token: text("access_token"),
    expires_at: integer("expires_at"),
    token_type: text("token_type"),
    scope: text("scope"),
    id_token: text("id_token"),
    session_state: text("session_state"),
  },
  (account) => ({
    compoundKey: primaryKey({
      columns: [account.provider, account.providerAccountId],
    }),
  })
);

export const sessions = sqliteTable('session', {
  sessionToken: text('sessionToken').primaryKey(),
  userId: text('userId').notNull().references(() => users.id, { onDelete: 'cascade' }),
  expires: integer('expires', { mode: 'timestamp_ms' }).notNull(),
});

export const verificationTokens = sqliteTable('verificationToken', {
  identifier: text('identifier').notNull(),
  token: text('token').notNull().unique(),
  expires: integer('expires', { mode: 'timestamp_ms' }).notNull(),
}, (table) => ({
  compoundKey: primaryKey({ columns: [table.identifier, table.token] }),
}));

export const usersRelations = relations(users, ({ many }) => ({
  accounts: many(accounts),
  sessions: many(sessions),
}));

export const accountsRelations = relations(accounts, ({ one }) => ({
  user: one(users, { fields: [accounts.userId], references: [users.id] }),
}));

export const sessionsRelations = relations(sessions, ({ one }) => ({
  user: one(users, { fields: [sessions.userId], references: [users.id] }),
}));
