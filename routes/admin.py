import fastapi
import bcrypt
#local
import db
import auth
from schema import AddUserRequest, TokenPayload
router = fastapi.APIRouter()

@router.post("/admin/add_user")
async def add_user(
    user:AddUserRequest,
    payload:TokenPayload=fastapi.Depends(auth.verify_token)

):  
    print("JwtToken Payload:",payload)

    if payload.role != "sys_admin":
        raise fastapi.HTTPException(status_code=401)
    
    async with db.getDictCursor() as cur:
        await cur.execute("SELECT id FROM users WHERE email = %s or username = %s", (user.email, user.username))
        row = await cur.fetchone()
        if row:
            raise fastapi.HTTPException(status_code=403, detail="Email or username already exists")


    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    async with db.getDictCursor() as cur:
        try:
            await cur.execute(
                "INSERT INTO users (email, username, password_hash, role) VALUES (%s, %s, %s, %s)",
                (user.email, user.username, user.hashed, user.role)
            )
        except Exception as e:
            raise fastapi.HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return fastapi.responses.JSONResponse(
        content={"msg": f"user {user.username} created successfully"},
        status_code=200
    )



@router.get("/admin/init_admin")
async def init_admin():
    email = "admin@gmail.com"
    username = "admin"
    password = "admin@1234"
    user_role = "sys_admin"
    
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
                "INSERT INTO users (email, username, password_hash, user_role) VALUES (%s, %s, %s %s)",
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
