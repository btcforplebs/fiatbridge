from fastapi import APIRouter, Depends, Request
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
from starlette.responses import HTMLResponse

fiatbridge_generic_router = APIRouter()

def fiatbridge_renderer():
    return template_renderer(["fiatbridge/templates"])

@fiatbridge_generic_router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return fiatbridge_renderer().TemplateResponse(
        "fiatbridge/index.html", {"request": request, "user": user.json()}
    )
