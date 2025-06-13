import React, { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { trpc } from '@/lib/trpc';
import { loadStripe } from '@stripe/stripe-js';
import { EmbeddedCheckoutProvider, EmbeddedCheckout } from '@stripe/react-stripe-js';
import { X, Check } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';

type PlanType = 'basic' | 'pro';
type BillingCycle = 'monthly' | 'yearly';
type Step = 'plan-selection' | 'billing-checkout';

const PRICING = {
  basic: {
    monthly: 9.99,
    yearly: 7.99,
    yearlyTotal: 95.88,
    features: [
      '200 content optimizations per month',
      'Advanced AI content generation',
      'SEO keyword optimization',
      'Content analysis & suggestions',
      'Priority support'
    ]
  },
  pro: {
    monthly: 29.99,
    yearly: 24.99,
    yearlyTotal: 299.88,
    features: [
      '1000 content optimizations per month',
      'Advanced AI content generation',
      'SEO keyword optimization',
      'Content analysis & suggestions',
      'Bulk content processing',
      'API access',
      'Priority support'
    ]
  }
};

const PlanSelection = ({
  onSelect,
}: {
  onSelect: (plan: PlanType) => void;
}) => {
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('pro');

  const handlePlanSelect = (plan: PlanType) => {
    setSelectedPlan(plan);
  };

  const handleContinue = () => {
    onSelect(selectedPlan);
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-4 p-6">
      <h2 className="text-xl font-semibold">Select your plan</h2>
      <div className="grid grid-cols-2 gap-4">
        <div 
          className={`border rounded-lg p-4 cursor-pointer hover:border-orange-500 transition-colors ${selectedPlan === 'basic' ? 'border-orange-500 bg-orange-50' : ''}`}
          onClick={() => handlePlanSelect('basic')}
        >
          <h3 className="font-medium mb-2">Basic</h3>
          <ul className="text-sm space-y-2">
            {PRICING.basic.features.map((feature, index) => (
              <li key={index} className="flex items-start">
                <span className="mr-2">-</span>
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div 
          className={`border rounded-lg p-4 cursor-pointer hover:border-orange-500 transition-colors ${selectedPlan === 'pro' ? 'border-orange-500 bg-orange-50' : ''}`}
          onClick={() => handlePlanSelect('pro')}
        >
          <h3 className="font-medium mb-2">Pro</h3>
          <ul className="text-sm space-y-2">
            {PRICING.pro.features.map((feature, index) => (
              <li key={index} className="flex items-start">
                <span className="mr-2">-</span>
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <Button
        variant="default"
        className="w-full shadow-none"
        onClick={handleContinue}
      >
        Continue
      </Button>
    </div>
  );
};

const SuccessPage = ({
  selectedPlan,
  selectedCycle,
  onClose,
}: {
  selectedPlan: PlanType;
  selectedCycle: BillingCycle;
  onClose: () => void;
}) => {
  return (
    <div className="w-full max-w-2xl mx-auto shadow-none space-y-6 p-6 text-center">
      <div className="flex justify-center">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mt-4">
          <Check className="h-8 w-8 text-green-600" />
        </div>
      </div>
      <div className="text-center space-y-2">
      <h2 className="text-2xl font-semibold">Subscription successful!</h2>
        <p className="text-muted-foreground">
          You have successfully subscribed to {selectedPlan === 'basic' ? 'Basic' : 'Pro'} plan.
        </p>
      </div>
      
      <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-left">
        <div className="flex text-sm text-muted-foreground justify-between">
          <span>Plan</span>
          <span className="font-medium">{selectedPlan === 'basic' ? 'Basic' : 'Pro'}</span>
        </div>
        <div className="flex text-sm text-muted-foreground justify-between">
          <span>Billing Cycle</span>
          <span className="font-medium">{selectedCycle === 'monthly' ? 'Monthly' : 'Yearly'}</span>
        </div>
        <div className="flex justify-between font-medium">
          <span>Total</span>
          <span>
            ${selectedCycle === 'monthly' 
              ? PRICING[selectedPlan].monthly 
              : PRICING[selectedPlan].yearlyTotal
            }
            {selectedCycle === 'yearly' ? ' / year' : ' / month'}
          </span>
        </div>
      </div>
      
      <p className="text-sm text-gray-500">
        You can now use advanced content optimization features!
      </p>
      
      <Button
        variant="default"
        className="w-full shadow-none"
        onClick={onClose}
      >
        Done
      </Button>
    </div>
  );
};

const BillingAndCheckout = ({
  selectedPlan,
  onCheckout,
  onBack,
  modalClose,
}: {
  selectedPlan: PlanType;
  onCheckout: (cycle: BillingCycle) => void;
  onBack: () => void;
  modalClose: () => void;
}) => {
  const planPricing = PRICING[selectedPlan];
  const yearlySavings = Math.round((planPricing.monthly * 12 - planPricing.yearlyTotal) * 100) / 100;
  const [selectedCycle, setSelectedCycle] = useState<BillingCycle>('yearly');
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [paymentStatus, setPaymentStatus] = useState<'processing' | 'succeeded' | 'failed' | null>(null);
  
  const utils = trpc.useUtils();
  
  const createEmbeddedSubscription = trpc.payment.createEmbeddedSubscription.useMutation({
    onSuccess: (data) => {
      setClientSecret(data.clientSecret);
      setIsLoading(false);
    },
    onError: (error) => {
      setError(error.message);
      setIsLoading(false);
    }
  });
  
  const handleCycleSelect = (cycle: BillingCycle) => {
    setSelectedCycle(cycle);
  };

  const handleCheckout = () => {
    setIsLoading(true);
    setError(null);
    
    onCheckout(selectedCycle);
    
    createEmbeddedSubscription.mutate({
      plan: selectedPlan,
      period: selectedCycle
    });
  };
  
  const handleBack = () => {
    if (clientSecret && paymentStatus !== 'succeeded') {
      setClientSecret(null);
    } else {
      onBack();
    }
  };
  
  const handleClose = () => {
    setClientSecret(null);
    setPaymentStatus(null);
    onBack();
  };
  
  const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!, {
    betas: ['custom_checkout_beta_6'],
  });
  
  const handleCheckoutComplete = useCallback(async () => {
    console.log('Checkout completed');
    setPaymentStatus('succeeded');
    
    await utils.user.getUserInfo.invalidate();
    await utils.user.getUserInfo.fetch();
  }, [utils]);
  
  if (paymentStatus === 'succeeded') {
    return <SuccessPage selectedPlan={selectedPlan} selectedCycle={selectedCycle} onClose={modalClose} />;
  }
  
  if (clientSecret) {
    console.log('Client secret:', clientSecret);
    console.log('Stripe instance:', stripePromise);
    
    return (
      <div className="w-full max-w-2xl mx-auto shadow-none">
        <EmbeddedCheckoutProvider 
          stripe={stripePromise} 
          options={{ 
            clientSecret,
            onComplete: handleCheckoutComplete
          }}
        >
          <div className="rounded-lg shadow-none">
            <EmbeddedCheckout />
          </div>
        </EmbeddedCheckoutProvider>
        <div className='w-full mx-auto px-6'>
           <Button
            variant="secondary"
            className="w-full shadow-none my-6"
            onClick={handleBack}
          >
            Back
        </Button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="w-full max-w-2xl mx-auto shadow-none space-y-4 p-6">
      <h2 className="text-xl font-semibold mb-4">Select billing cycle</h2>
      
      <div className="grid grid-cols-2 gap-4">
        <div 
          className={`border rounded-lg p-4 cursor-pointer space-y-2 hover:border-orange-500 transition-colors ${selectedCycle === 'monthly' ? 'border-orange-500 bg-orange-50' : ''}`}
          onClick={() => handleCycleSelect('monthly')}
        >
          <h3 className="font-medium mb-2">Monthly</h3>
          <div className="text-2xl font-semibold">${planPricing.monthly}</div>
          <div className="text-sm text-muted-foreground">per month</div>
        </div>
        
        <div className={`border rounded-lg overflow-hidden cursor-pointer space-y-2 hover:border-orange-500 transition-colors ${selectedCycle === 'yearly' ? 'border-orange-500 bg-orange-50' : ''}`}>
        <div 
          className="space-y-2 p-4"
          onClick={() => handleCycleSelect('yearly')}
        >
          <h3 className="font-medium mb-2">Yearly</h3>
          <div className="text-2xl font-semibold">${planPricing.yearly}</div>
          <div className="text-sm text-muted-foreground">per month</div>
          <div className="text-sm">${planPricing.yearlyTotal} billed yearly</div>
        </div>
        <div className="bg-orange-500 text-white text-xs p-2 text-center">
            Save ${yearlySavings} per year
        </div>
        </div>

      </div>
      
      <div className="bg-gray-50 p-4 rounded-lg space-y-2">
        <div className="flex text-sm text-muted-foreground justify-between">
          <span>Plan</span>
          <span className="font-medium">{selectedPlan === 'basic' ? 'Basic' : 'Pro'}</span>
        </div>
        <div className="flex justify-between font-medium">
          <span>Total</span>
          <span>
            ${selectedCycle === 'monthly' 
              ? PRICING[selectedPlan].monthly 
              : PRICING[selectedPlan].yearlyTotal
            }
            {selectedCycle === 'yearly' ? ' / year' : ' / month'}
          </span>
        </div>
        <p className="text-xs text-muted-foreground">You can cancel the plan at any time.</p>
      </div>
      
      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4">
          {error}
        </div>
      )}
      
      <div className="flex space-x-4">
        <Button
          variant="secondary"
          className="shadow-none"
          onClick={onBack}
          disabled={isLoading}
        >
          Back
        </Button>
        <Button
          variant="default"
          className="flex-1 shadow-none"
          onClick={handleCheckout}
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Upgrade now'}
        </Button>
      </div>
    </div>
  );
};

interface PriceModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PriceModal: React.FC<PriceModalProps> = ({ isOpen, onClose }) => {
  const [step, setStep] = useState<Step>('plan-selection');
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('pro');
  const [selectedCycle, setSelectedCycle] = useState<BillingCycle>('yearly');
  
  const handlePlanSelect = (plan: PlanType) => {
    setSelectedPlan(plan);
    setStep('billing-checkout');
  };
  
  const handleCycleSelect = (cycle: BillingCycle) => {
    setSelectedCycle(cycle);
  };
  
  const handleBack = () => {
    if (step === 'billing-checkout') {
      setStep('plan-selection');
    }
  };
  
  const resetModal = () => {
    setStep('plan-selection');
    setSelectedPlan('pro');
    setSelectedCycle('yearly');
  };
  
  const handleClose = () => {
    onClose();
    setTimeout(resetModal, 300);
  };
  
  return (
    <Dialog open={isOpen} onOpenChange={handleClose} modal={true}>
      <DialogContent 
        className="sm:max-w-2xl max-h-[80vh] overflow-y-auto p-0 rounded-2xl bg-white"
        onPointerDownOutside={(e) => e.preventDefault()}
        onEscapeKeyDown={(e) => e.preventDefault()}
      >
        
        {step === 'plan-selection' && (
          <PlanSelection onSelect={handlePlanSelect} />
        )}
        
        {step === 'billing-checkout' && (
          <BillingAndCheckout
            selectedPlan={selectedPlan}
            onCheckout={handleCycleSelect}
            onBack={handleBack}
            modalClose={handleClose}
          />
        )}
      </DialogContent>
    </Dialog>
  );
};

export default PriceModal;
