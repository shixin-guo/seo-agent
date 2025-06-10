import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { type NextRequest } from 'next/server';

import { appRouter } from '@/server/api/root';
import { createTRPCContext } from '@/server/api/trpc';

const handler = async (req: NextRequest) => {
  try {
    return await fetchRequestHandler({
      endpoint: '/api/trpc',
      req,
      router: appRouter,
      createContext: () => createTRPCContext({ req }),
      onError:
        process.env.NODE_ENV === 'development'
          ? ({ path, error }) => {
              console.error(
                `❌ tRPC failed on ${path ?? '<no-path>'}: ${error.message}`
              );
            }
          : undefined,
    });
  } catch (error) {
    console.error('tRPC handler error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
};

export { handler as GET, handler as POST };
