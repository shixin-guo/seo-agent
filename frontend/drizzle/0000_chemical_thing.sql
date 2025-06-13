CREATE TABLE `account` (
	`userId` text NOT NULL,
	`type` text NOT NULL,
	`provider` text NOT NULL,
	`providerAccountId` text NOT NULL,
	`refresh_token` text,
	`access_token` text,
	`expires_at` integer,
	`token_type` text,
	`scope` text,
	`id_token` text,
	`session_state` text,
	PRIMARY KEY(`provider`, `providerAccountId`),
	FOREIGN KEY (`userId`) REFERENCES `user`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `session` (
	`sessionToken` text PRIMARY KEY NOT NULL,
	`userId` text NOT NULL,
	`expires` integer NOT NULL,
	FOREIGN KEY (`userId`) REFERENCES `user`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `user` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text,
	`email` text,
	`emailVerified` integer,
	`image` text,
	`usedCredits` integer DEFAULT 0,
	`planType` text DEFAULT 'FREE',
	`storageUsed` integer DEFAULT 0,
	`storageLimit` integer DEFAULT 104857600,
	`monthlyCredits` integer DEFAULT 50,
	`lastCreditReset` integer,
	`planStartDate` integer,
	`planEndDate` integer,
	`stripeCustomerId` text,
	`stripeSubscriptionId` text,
	`subscriptionStatus` text(20),
	`createdAt` integer DEFAULT (strftime('%s','now') * 1000),
	`updatedAt` integer DEFAULT (strftime('%s','now') * 1000)
);
--> statement-breakpoint
CREATE UNIQUE INDEX `user_email_unique` ON `user` (`email`);--> statement-breakpoint
CREATE UNIQUE INDEX `user_stripeCustomerId_unique` ON `user` (`stripeCustomerId`);--> statement-breakpoint
CREATE TABLE `verificationToken` (
	`identifier` text NOT NULL,
	`token` text NOT NULL,
	`expires` integer NOT NULL,
	PRIMARY KEY(`identifier`, `token`)
);
--> statement-breakpoint
CREATE UNIQUE INDEX `verificationToken_token_unique` ON `verificationToken` (`token`);--> statement-breakpoint
CREATE TABLE `creditLog` (
	`id` text PRIMARY KEY NOT NULL,
	`userId` text NOT NULL,
	`amount` integer NOT NULL,
	`balance` integer NOT NULL,
	`action` text NOT NULL,
	`description` text,
	`createdAt` integer DEFAULT (strftime('%s','now') * 1000),
	FOREIGN KEY (`userId`) REFERENCES `user`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `invoice` (
	`id` text PRIMARY KEY NOT NULL,
	`userId` text NOT NULL,
	`stripeInvoiceId` text NOT NULL,
	`stripeSubscriptionId` text,
	`amount` integer NOT NULL,
	`currency` text DEFAULT 'usd',
	`status` text NOT NULL,
	`billingReason` text,
	`periodStart` integer,
	`periodEnd` integer,
	`paymentMethod` text,
	`invoiceUrl` text,
	`invoicePdf` text,
	`metadata` text,
	`createdAt` integer DEFAULT (strftime('%s','now') * 1000),
	FOREIGN KEY (`userId`) REFERENCES `user`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `invoice_stripeInvoiceId_unique` ON `invoice` (`stripeInvoiceId`);