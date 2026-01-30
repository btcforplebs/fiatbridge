from fastapi import APIRouter, Depends, HTTPException
from lnbits.core.models import WalletTypeInfo
from lnbits.core.models.payments import CreateInvoice
from lnbits.core.services.payments import create_fiat_invoice
from lnbits.decorators import require_invoice_key
from lnbits.settings import settings
from .models import CreateBridgeCheckout

fiatbridge_api_router = APIRouter(prefix="/api/v1", tags=["Fiat Bridge API"])


def calculate_customer_fee(amount: float, provider_name: str = "stripe") -> tuple[float, float]:
    """
    Calculate the fee that the customer will pay.
    Returns (total_amount_with_fee, fee_amount)
    """
    limits = settings.get_fiat_provider_limits(provider_name)
    if not limits or not limits.service_fee_wallet_id:
        return amount, 0.0
    
    fee_percent = limits.service_fee_percent
    fee_amount = amount * (fee_percent / 100.0)
    
    # Check if there's a max fee cap (convert from sats to USD approximately)
    # For simplicity, we apply the percentage fee to the USD amount
    total_amount = amount + fee_amount
    
    return round(total_amount, 2), round(fee_amount, 2)


@fiatbridge_api_router.post("/checkout")
async def api_fiatbridge_checkout(
    data: CreateBridgeCheckout,
    wallet: WalletTypeInfo = Depends(require_invoice_key)
):
    """
    Create a Stripe checkout session for card payments.
    
    If a service fee is configured, the fee is ADDED to the checkout amount
    so the customer pays the fee, not the merchant.
    
    Example: $10.00 product + 3% fee = $10.30 checkout amount
    - Customer pays: $10.30
    - Service fee wallet receives: $0.30 worth of BTC
    - Merchant wallet receives: $10.00 worth of BTC
    
    Returns a checkout_url that redirects the user to Stripe's hosted checkout page.
    """
    try:
        # Calculate fee and add to amount
        base_amount = data.amount
        total_amount, fee_amount = calculate_customer_fee(base_amount)
        
        # Build memo with fee info if applicable
        checkout_memo = data.memo
        if fee_amount > 0:
            checkout_memo = f"{data.memo} (includes ${fee_amount:.2f} processing fee)"
        
        # Create the fiat invoice using core services. 
        # This automatically:
        # 1. Registers the payment in the DB (fixes the webhook error)
        # 2. Calls the Stripe provider
        # 3. Handles Satoshi conversion for the ledger
        invoice_data = CreateInvoice(
            amount=total_amount,
            unit="USD",
            memo=checkout_memo,
            extra={
                "fiat_method": "checkout",
                "checkout": {
                    "success_url": data.success_url,
                    "line_item_name": checkout_memo,
                    "metadata": {
                        "base_amount": str(base_amount),
                        "fee_amount": str(fee_amount),
                        "merchant_wallet_id": wallet.wallet.id
                    }
                }
            },
            fiat_provider="stripe"
        )
        
        payment = await create_fiat_invoice(
            wallet_id=wallet.wallet.id,
            invoice_data=invoice_data
        )
        
        # Extract the details from the created payment object
        # The 'checking_id' now has the 'fiat_stripe_' prefix correctly
        return {
            "checkout_url": payment.extra.get("fiat_payment_request"),
            "payment_hash": payment.payment_hash,
            "session_id": payment.extra.get("fiat_checking_id"),
            "base_amount": base_amount,
            "fee_amount": fee_amount,
            "total_amount": total_amount
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
