import { GET, POST } from '@/server/auth';

const safeGET = GET || (() => new Response('Auth not configured', { status: 500 }));
const safePOST = POST || (() => new Response('Auth not configured', { status: 500 }));

export { safeGET as GET, safePOST as POST };
