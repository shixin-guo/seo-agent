import { createTRPCRouter } from '@/server/api/trpc';
import { paymentRouter } from './routers/payment';
import { userRouter } from './routers/user';

export const appRouter = createTRPCRouter({
  payment: paymentRouter,
  user: userRouter,
});

export type AppRouter = typeof appRouter;
