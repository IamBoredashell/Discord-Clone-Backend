import jwt 
import fastapi

# local
import server

security = HTTPBearer()

async def verify_token(credentials: str = Depends(security)):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,JWTSECRETKEY, algorithm=[JWTALGO])
        return payload
    except JWTError:
        raise HTTPException(status_code=401)

