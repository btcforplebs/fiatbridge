# Fiat Bridge Extension for LNbits

A public bridge that allows external websites to request Stripe checkout sessions using your LNbits wallet without exposing your admin keys.

## How it Works

The Fiat Bridge acts as a secure intermediary between your website and the Stripe payment gateway, leveraging LNbits' core payment engine.

1. **API Call**: Your website makes a simple POST request to the Fiat Bridge API endpoint using an **Invoice Key**.
2. **Bridge Request**: The extension receives the request and forwards it to the Stripe API.
3. **Checkout Redirection**: Stripe generates a checkout session and returns a URL. The Fiat Bridge passes this `checkout_url` back to your website.
4. **User Payment**: Your website redirects the user to the Stripe checkout page where they complete the card payment.
5. **Return**: After a successful checkout, the user is automatically sent back to your specified `success_url`.
6. **Backend Fulfillment**:
    - The transaction is tracked and memoed within LNbits.
    - The bitcoin equivalent (at the time of payment) is deposited into the LNbits wallet associated with the used **Invoice Key**.

## Use Cases

The Fiat Bridge is ideal for scenarios where you want to accept legacy card payments while keeping your accounting and settlement in Bitcoin/LNbits.

- **Simple Web Shops**: Sell digital or physical goods on a custom website. Users pay with cards, and you receive Bitcoin instantly in your LNbits wallet.
- **Physical Kiosks**: Use a tablet or phone as a point-of-sale terminal. Generate a checkout link for the customer to pay on their own device via Stripe.
- **Donation Platforms**: Let supporters contribute via familiar card payments. The bridge handles the conversion and deposits sats into your specified wallet.
- **Service Providers**: Invoice clients for services (consulting, design, etc.) and receive payment in Bitcoin without them needing to know how to use a Lightning wallet.
- **Secure Backend Integration**: Integrate card payments into your app without ever touching sensitive Stripe API keys or card data on your own frontend.

## Transitioning to a Bitcoin Standard

The Fiat Bridge is more than just a payment gateway; it's a strategic tool for businesses and individuals moving towards a Bitcoin standard:

- **Immediate Settlement in Sats**: Avoid the volatility and delays of legacy banking. Every card payment is converted and settled instantly in your own Bitcoin wallet.
- **Legacy Compatibility**: Onboard customers who aren't yet ready for Lightning by providing a familiar checkout experience (Stripe), while you benefit from Bitcoin's superior monetary properties.
- **Reduced Banking Dependency**: Minimize the amount of capital held in traditional financial institutions. Use Bitcoin as your primary unit of account and store of value.
- **Seamless Accounting**: Consolidate all your sales—whether via Lightning or Card—into a single LNbits dashboard, simplifying your financial tracking and reporting.

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
