import fastapi
import bcrypt
#local
import db
import auth

router = fastapi.APIRouter()

@router.post("/admin/add_user")
async def add_user(
        data: dict = fastapi.Body(...),
        payload: dict = fastapi.Depends(auth.verify_token)
):  
    print("JwtToken Payload:",payload)
    #  TO DO :check admin rights from JWT and verify from DB instead of username
    if payload.get("username") != "admin":
        raise fastapi.HTTPException(status_code=403)

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        raise fastapi.HTTPException(status_code=400)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    async with db.getDictCursor() as cur:
        try:
            await cur.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                (email, username, hashed)
            )
        except Exception as e:
            raise fastapi.HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return fastapi.responses.JSONResponse(
        content={"msg": f"user {username} created successfully"},
        status_code=200
    )



@router.get("/admin/init_admin")
async def init_admin():
    email = "admin@gmail.com"
    username = "admin"
    password = "admin"
    
    async with db.getDictCursor() as cur:
        # check if admin already exists
        await cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = await cur.fetchone()

        if row:
            return fastapi.responses.JSONResponse(
                content={"msg": "Admin already exists"},
                status_code=200
            )

        # hash password with salt
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        try:
            await cur.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                (email, username, hashed)
            )
        except Exception as e:
            return fastapi.responses.JSONResponse(
                content={"msg": f"DB error: {str(e)}"},
                status_code=500
            )

    return fastapi.responses.JSONResponse(
        content={"msg": "Admin user created successfully"},
        status_code=200
    )
