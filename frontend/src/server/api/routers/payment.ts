import { createTRPCRouter, publicProcedure, protectedProcedure } from "../trpc";
import { z } from "zod";
import Stripe from "stripe";
import { TRPCError } from "@trpc/server";
import { users } from "@/server/db/schema/auth";
import { invoices } from "@/server/db/schema/premium";
import { eq } from "drizzle-orm";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2025-05-28.basil",
});

export const paymentRouter = createTRPCRouter({
  createBillingPortalSession: protectedProcedure
    .mutation(async ({ ctx }) => {
      try {
        if (!ctx.session?.user) {
          throw new TRPCError({
            code: "UNAUTHORIZED",
            message: "You must be logged in to access billing portal",
          });
        }
        
        const userId = ctx.session.user.id;
        
        const userResults = await ctx.db.select()
          .from(users)
          .where(eq(users.id, userId));
        
        const user = userResults[0];
        if (!user) {
          throw new TRPCError({
            code: "NOT_FOUND",
            message: "User not found",
          });
        }
        
        if (!user.stripeCustomerId) {
          throw new TRPCError({
            code: "BAD_REQUEST",
            message: "No Stripe customer found for this user",
          });
        }
        
        const portalSession = await stripe.billingPortal.sessions.create({
          customer: user.stripeCustomerId,
          return_url: `${process.env.NEXTAUTH_URL}/content-optimizer`,
        });
        
        return { url: portalSession.url };
      } catch (error) {
        console.error("Error creating billing portal session:", error);
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: `Error creating billing portal session: ${(error as Error).message}`,
        });
      }
    }),

  createEmbeddedSubscription: protectedProcedure
    .input(
      z.object({
        plan: z.enum(["basic", "pro"]),
        period: z.enum(["monthly", "yearly"]),
      })
    )
    .mutation(async ({ ctx, input }) => {
      if (!ctx.session?.user?.id) {
        throw new TRPCError({
          code: "UNAUTHORIZED",
          message: "You must be logged in to subscribe",
        });
      }

      const userId = ctx.session.user.id;
      const userEmail = ctx.session.user.email!;
      
      try {
        let stripeCustomerId: string;
        
        const userResults = await ctx.db.select()
          .from(users)
          .where(eq(users.id, userId));
        
        const user = userResults[0];
        
        if (user?.stripeCustomerId) {
          stripeCustomerId = user.stripeCustomerId;
        } else {
          const customer = await stripe.customers.create({
            email: userEmail,
            metadata: { userId },
          });
          stripeCustomerId = customer.id;
          
          await ctx.db.update(users)
            .set({ stripeCustomerId })
            .where(eq(users.id, userId));
        }

        const priceIds = {
          basic: {
            monthly: process.env.BASIC_MONTHLY_PRICE_ID!,
            yearly: process.env.BASIC_YEARLY_PRICE_ID!,
          },
          pro: {
            monthly: process.env.PRO_MONTHLY_PRICE_ID!,
            yearly: process.env.PRO_YEARLY_PRICE_ID!,
          },
        };

        const session = await stripe.checkout.sessions.create({
          ui_mode: 'embedded',
          customer: stripeCustomerId,
          line_items: [
            {
              price: priceIds[input.plan][input.period],
              quantity: 1,
            },
          ],
          mode: 'subscription',
          return_url: `${process.env.NEXTAUTH_URL}/content-optimizer?session_id={CHECKOUT_SESSION_ID}`,
          metadata: {
            userId,
            plan: input.plan,
            period: input.period,
          },
        });

        return { clientSecret: session.client_secret };
      } catch (error) {
        console.error("Error creating embedded subscription:", error);
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: `Error creating embedded subscription: ${(error as Error).message}`,
        });
      }
    }),

  updateUserPlanFromWebhook: publicProcedure
    .input(
      z.object({
        userId: z.string(),
        plan: z.string(),
        period: z.string(),
        planStartDate: z.number(),
        planEndDate: z.number(),
        shouldResetCredits: z.boolean().optional(),
        stripeCustomerId: z.string().optional(),
        stripeSubscriptionId: z.string().optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      try {
        const planCredits = {
          basic: 200,
          pro: 1000,
        };

        const updateData: any = {
          planType: input.plan.toUpperCase(),
          planStartDate: input.planStartDate,
          planEndDate: input.planEndDate,
          subscriptionStatus: 'active',
          updatedAt: new Date(),
        };

        if (input.shouldResetCredits) {
          updateData.monthlyCredits = planCredits[input.plan as keyof typeof planCredits] || 50;
          updateData.usedCredits = 0;
          updateData.lastCreditReset = input.planStartDate;
        }

        if (input.stripeCustomerId) {
          updateData.stripeCustomerId = input.stripeCustomerId;
        }

        if (input.stripeSubscriptionId) {
          updateData.stripeSubscriptionId = input.stripeSubscriptionId;
        }

        await ctx.db.update(users)
          .set(updateData)
          .where(eq(users.id, input.userId));

        return { success: true };
      } catch (error) {
        console.error("Error updating user plan:", error);
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: `Error updating user plan: ${(error as Error).message}`,
        });
      }
    }),

  saveInvoice: publicProcedure
    .input(
      z.object({
        userId: z.string(),
        stripeInvoiceId: z.string(),
        stripeSubscriptionId: z.string().optional(),
        amount: z.number(),
        currency: z.string().default('usd'),
        status: z.string(),
        billingReason: z.string().optional(),
        periodStart: z.number().optional(),
        periodEnd: z.number().optional(),
        paymentMethod: z.string().optional(),
        invoiceUrl: z.string().optional(),
        invoicePdf: z.string().optional(),
        metadata: z.string().optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      try {
        await ctx.db.insert(invoices).values({
          userId: input.userId,
          stripeInvoiceId: input.stripeInvoiceId,
          stripeSubscriptionId: input.stripeSubscriptionId,
          amount: input.amount,
          currency: input.currency,
          status: input.status,
          billingReason: input.billingReason,
          periodStart: input.periodStart,
          periodEnd: input.periodEnd,
          paymentMethod: input.paymentMethod,
          invoiceUrl: input.invoiceUrl,
          invoicePdf: input.invoicePdf,
          metadata: input.metadata,
        } as any);

        return { success: true };
      } catch (error) {
        console.error("Error saving invoice:", error);
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: `Error saving invoice: ${(error as Error).message}`,
        });
      }
    }),
});
