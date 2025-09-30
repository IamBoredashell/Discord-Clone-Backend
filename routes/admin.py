import fastapi
import asyncio
import datetime 
import bcrypt
# Local
import db 
import server 
import auth

router = APIRouter()

@router.get("/admin/add_user")
async def add_user(
        data: dict = Body(...),
        payload: dict = Depends(verify_token)
):
    if payload.get("username")!="admin":
        raise HTTPException(status_code=403)
    email=data.get("email")
    username=data.get("username")
    password=data.get("password")

    if not email or not username or not password:
        raise HTTPException(status_code=400)
    salt=bcrypt.gensalt()
    hash=bcrypt.hashpw(password.encode(),salt).decode()
    
    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            try:
                await cur.execute(
                    "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                    (email, username, hash)"
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    return JSONResponse(
        content={"msg":f"user{username} created successfully"},
        status_code=200
    )

