import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { type NextRequest } from 'next/server';

const createSafeHandler = () => {
  try {
    const { appRouter } = require('@/server/api/root');
    const { createTRPCContext } = require('@/server/api/trpc');

    return async (req: NextRequest) => {
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
  } catch (error) {
    console.warn('tRPC initialization failed during build:', error);
    return async () => new Response('tRPC not available during build', { status: 503 });
  }
};

const safeHandler = createSafeHandler();
const GET = safeHandler || (() => new Response('tRPC not available', { status: 503 }));
const POST = safeHandler || (() => new Response('tRPC not available', { status: 503 }));

export { GET, POST };
