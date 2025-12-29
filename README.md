# Fiat Bridge Extension for LNbits

A public bridge that allows external websites to request Stripe checkout sessions using your LNbits wallet without exposing your admin keys.

## Installation

1. Copy this `fiatbridge` folder into your LNbits `lnbits/extensions/` directory.
2. Restart LNbits.
3. Enable "Fiat Bridge" in the extensions list.

## How to Use

1. Go to the Fiat Bridge dashboard in LNbits.
2. Copy your **Invoice Key**.
3. From your website's backend (or a secure bridge), send a POST request:

**Endpoint:** `https://your-lnbits.com/fiatbridge/api/v1/checkout`
**Headers:** `X-Api-Key: <your_invoice_key>`

**Body:**
```json
{
  "amount": 10.00,
  "memo": "Payment for Coffee",
  "success_url": "https://yourshop.com/success",
  "cancel_url": "https://yourshop.com/cancel"
}
```

The API will return a `checkout_url` which you can use to redirect the user to Stripe.
