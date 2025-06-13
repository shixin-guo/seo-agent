import { NextRequest, NextResponse } from "next/server";
import Stripe from "stripe";
import { createTRPCProxyClient, httpBatchLink } from "@trpc/client";
import { AppRouter } from "@/server/api/root";
import superjson from "superjson";

const createTRPCClient = () => {
  const url = `${process.env.NEXTAUTH_URL}/api/trpc`;
  
  return createTRPCProxyClient<AppRouter>({
    links: [
      httpBatchLink({
        url,
        transformer: superjson,
      }),
    ],
  });
};

export async function POST(req: NextRequest) {
  if (!process.env.STRIPE_SECRET_KEY || !process.env.STRIPE_WEBHOOK_SECRET) {
    console.error("Missing Stripe environment variables");
    return NextResponse.json({ error: "Server configuration error" }, { status: 500 });
  }

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
    apiVersion: "2025-05-28.basil",
  });

  const body = await req.text();
  const signature = req.headers.get("stripe-signature") as string;

  let event: Stripe.Event;

  try {
    event = await stripe.webhooks.constructEventAsync(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    const error = err as Error;
    console.error(`Webhook signature verification failed: ${error.message}`);
    return NextResponse.json({ error: error.message }, { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;
    
    console.log("Processing checkout.session.completed event:", JSON.stringify(session, null, 2));
    
    if (!session.metadata) {
      console.error("No metadata found in session:", session.id);
      return NextResponse.json({ error: "No metadata found" }, { status: 400 });
    }

    const metadata = session.metadata as { 
      userId: string; 
      plan?: string; 
      period?: string;
    };
    
    const userId = metadata.userId;
    const plan = metadata.plan || 'basic';
    const period = metadata.period || 'monthly';
    
    console.log(`Extracted metadata: userId=${userId}, plan=${plan}, period=${period}`);

    if (session.mode === "subscription" && userId && plan) {
      try {
        const now = new Date();
        const planStartDate = now.getTime();
        let planEndDate: number;

        if (period === "monthly") {
          const endDate = new Date(now);
          endDate.setMonth(endDate.getMonth() + 1);
          planEndDate = endDate.getTime();
        } else {
          const endDate = new Date(now);
          endDate.setFullYear(endDate.getFullYear() + 1);
          planEndDate = endDate.getTime();
        }

        console.log(`Updating user ${userId} to ${plan} plan (${period})`);
        console.log(`Plan dates: start=${new Date(planStartDate).toISOString()}, end=${new Date(planEndDate).toISOString()}`);
        
        try {
          const trpc = createTRPCClient();
          
          const result = await trpc.payment.updateUserPlanFromWebhook.mutate({
            userId,
            plan,
            period,
            planStartDate,
            planEndDate,
            shouldResetCredits: true,
            stripeCustomerId: session.customer ? String(session.customer) : undefined,
            stripeSubscriptionId: session.subscription ? String(session.subscription) : undefined,
          });
          
          console.log(`User plan updated successfully via tRPC: ${JSON.stringify(result)}`);
          return NextResponse.json({ success: true });
        } catch (trpcError) {
          const errorMessage = trpcError instanceof Error ? trpcError.message : String(trpcError);
          console.error(`Error calling tRPC endpoint: ${errorMessage}`);
          return NextResponse.json({ error: `Error updating user plan: ${errorMessage}` }, { status: 500 });
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error(`Error updating user plan: ${errorMessage}`);
        return NextResponse.json({ error: `Failed to update user plan: ${errorMessage}` }, { status: 500 });
      }
    }
  }

  return NextResponse.json({ received: true });
}
