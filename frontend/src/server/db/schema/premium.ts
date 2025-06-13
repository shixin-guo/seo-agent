import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
import { relations, sql } from 'drizzle-orm';
import { users } from './auth';

export const creditLogs = sqliteTable('creditLog', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  userId: text('userId').notNull().references(() => users.id, { onDelete: 'cascade' }),
  amount: integer('amount').notNull(),
  balance: integer('balance').notNull(),
  action: text('action').notNull(),
  description: text('description'),
  createdAt: integer("createdAt", { mode: "timestamp_ms" }).default(sql`(strftime('%s','now') * 1000)`),
});

export const invoices = sqliteTable('invoice', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  userId: text('userId').notNull().references(() => users.id, { onDelete: 'cascade' }),
  stripeInvoiceId: text('stripeInvoiceId').notNull().unique(),
  stripeSubscriptionId: text('stripeSubscriptionId'),
  amount: integer('amount').notNull(),
  currency: text('currency').default('usd'),
  status: text('status').notNull(),
  billingReason: text('billingReason'),
  periodStart: integer('periodStart', { mode: 'timestamp_ms' }),
  periodEnd: integer('periodEnd', { mode: 'timestamp_ms' }),
  paymentMethod: text('paymentMethod'),
  invoiceUrl: text('invoiceUrl'),
  invoicePdf: text('invoicePdf'),
  metadata: text('metadata'),
  createdAt: integer("createdAt", { mode: "timestamp_ms" }).default(sql`(strftime('%s','now') * 1000)`),
});

export const creditLogsRelations = relations(creditLogs, ({ one }) => ({
  user: one(users, { fields: [creditLogs.userId], references: [users.id] }),
}));

export const invoicesRelations = relations(invoices, ({ one }) => ({
  user: one(users, { fields: [invoices.userId], references: [users.id] }),
}));
