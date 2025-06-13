import { createTRPCRouter, protectedProcedure } from '../trpc';
import { users } from '@/server/db/schema/auth';
import { eq } from 'drizzle-orm';

export const userRouter = createTRPCRouter({
  getUserInfo: protectedProcedure
    .query(async ({ ctx }) => {
      const userId = ctx.session.user.id;
      
      const userResults = await ctx.db.select()
        .from(users)
        .where(eq(users.id, userId));
      
      const user = userResults[0];
      if (!user) {
        throw new Error('User not found');
      }
      
      return {
        id: user.id,
        name: user.name,
        email: user.email,
        planType: user.planType,
        subscriptionStatus: user.subscriptionStatus,
        monthlyCredits: user.monthlyCredits,
        usedCredits: user.usedCredits,
        planEndDate: user.planEndDate,
      };
    }),
});
