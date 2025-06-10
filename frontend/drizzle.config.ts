import type { Config } from 'drizzle-kit';

export default {
  schema: './src/server/db/schema/*',
  out: './drizzle',
  dialect: 'sqlite',
  dbCredentials: {
    url: process.env.DATABASE_URL || 'file:./dev.db',
  },
} satisfies Config;
