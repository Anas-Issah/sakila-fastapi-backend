from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import APIRouter,Request

router = APIRouter(
    prefix="/oauth",
    tags=["AUTHORIZATION"]
)

oauth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://127.0.0.1:8000/oauth/authorize",
    tokenUrl="http://127.0.0.1:8000/oauth/token"
)

@router.get("/oauth/authorize")
async def authorize(client_id:str,redirect_uri:str,
                    state:str):

    auth_code = "local_auth_code"

    redirect_uri = f"{redirect_uri}?code={auth_code}"

    if state:

        redirect_uri += f"&state={state}"

    return 

@router.post("/oauth/token")
async def token(request:Request):

    form_data = await request.form()
    code = form_data.get("code")
    grant_type = form_data.get("grant_type")

    if grant_type != "authorization_code" or code != "local_auth_code":
        raise ValueError

    return {
        "access_token": "local-secret-token-xyz",
        "token_type": "bearer"
    }