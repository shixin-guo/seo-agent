const createAuthHandlers = () => {
  try {
    const NextAuth = require("next-auth").default;
    const Google = require("next-auth/providers/google").default;

    const authConfig = {
      providers: [
        Google({
          clientId: process.env.GOOGLE_CLIENT_ID || "dummy-client-id",
          clientSecret: process.env.GOOGLE_CLIENT_SECRET || "dummy-client-secret",
        })
      ],
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
    };

    const auth = NextAuth(authConfig);
    return auth.handlers;
  } catch (error) {
    console.warn('NextAuth initialization failed during build:', error);
    return {
      GET: () => new Response('Auth not available during build', { status: 503 }),
      POST: () => new Response('Auth not available during build', { status: 503 }),
    };
  }
};

const handlers = createAuthHandlers();
const GET = handlers?.GET || (() => new Response('Auth not available', { status: 503 }));
const POST = handlers?.POST || (() => new Response('Auth not available', { status: 503 }));

export { GET, POST };
