import fastapi
import bcrypt
from fastapi.responses import JSONResponse
from db import pool

router = fastapi.APIRouter()

@router.get("/admin/init_admin")
async def init_admin():
    email = "admin@gmail.com"
    username = "admin"
    password = "admin"

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            # check if admin already exists
            await cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            row = await cur.fetchone()

            if row:
                return JSONResponse(
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
                return JSONResponse(
                    content={"msg": f"DB error: {str(e)}"},
                    status_code=500
                )

    return JSONResponse(
        content={"msg": "Admin user created successfully"},
        status_code=200
    )
