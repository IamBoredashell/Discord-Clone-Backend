import fastapi
import jwt

# local
import server

security = fastapi.security.HTTPBearer()

async def verify_token(credentials: fastapi.Depends = fastapi.Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            server.JWTSECRETKEY,
            algorithms=[server.JWTALGO]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise fastapi.HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise fastapi.HTTPException(status_code=401, detail="Invalid token")
