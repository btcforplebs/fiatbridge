from pydantic import BaseModel

class CreateBridgeCheckout(BaseModel):
    amount: float
    memo: str
    success_url: str
    cancel_url: str | None = None
