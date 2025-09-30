import db 
import server
import bcrypt
import jwt 



@app.post("/login")
async def login(data: dict = Body(...)):
    email=data.get("email")
    password=data.get("password")
    if not password or not email: 
        raise HTTPexception(status_code=400)
    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute("SELECT FROM users WHERE email = %s", (email,))
            row=await cur.fetchone()
            if row:
                hash=row["password_hash"]
                user_id=row["id"]
                if bcrypt.checkpw(password.encode(),hash.encode()):
                    expire=datetime.utcnow()+timedelta(minutes=5)
                    token=jwt.encode({"sub":user_id,"username":username,"exp":expire},JWTSECRETKEY, algorithm=JWTALGO)
                    return  JSONResponse(content={"Token":token},status_code=200)
    raise HTTPException(status_code=401")


