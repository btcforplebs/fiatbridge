from fastapi import APIRouter, Depends, HTTPException, Request
from lnbits.core.models import WalletTypeInfo
from lnbits.core.views.payment_api import api_payments_create
from lnbits.core.models.payments import CreateInvoice
from lnbits.decorators import require_invoice_key
from .models import CreateBridgeCheckout

fiatbridge_api_router = APIRouter(prefix="/api/v1", tags=["Fiat Bridge API"])

@fiatbridge_api_router.post("/checkout")
async def api_fiatbridge_checkout(
    data: CreateBridgeCheckout,
    # In a real version, we'd use a custom scoped token here
    wallet: WalletTypeInfo = Depends(require_invoice_key)
):
    # This logic matches what we built in server.js
    try:
        invoice_data = CreateInvoice(
            out=False,
            amount=data.amount,
            unit="USD",
            memo=data.memo,
            fiat_provider="stripe",
            extra={
                "checkout": {
                    "success_url": data.success_url
                }
            }
        )
        
        # We call the core payment engine directly
        payment = await api_payments_create(invoice_data, wallet)
        
        return {
            "checkout_url": payment.payment_request,
            "payment_hash": payment.payment_hash
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
