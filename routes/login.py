import fastapi
import bcrypt
import jwt
import datetime
import psycopg
#local
import db
from config import JWTALGO, JWTSECRETKEY
router = fastapi.APIRouter()

@router.post("/login")
async def login(data: dict = fastapi.Body(...)):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise fastapi.HTTPException(status_code=400)

    async with db.getDictCursor() as cur:
        await cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = await cur.fetchone()

        if row:
            hash = row["password_hash"]
            user_id = row["id"]
            username = row["username"]

            if bcrypt.checkpw(password.encode(), hash.encode()):
                expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
                token = jwt.encode(
                    {"sub": str(user_id), "username": username, "exp": expire},
                    JWTSECRETKEY,
                    algorithm=JWTALGO
                )
                return fastapi.responses.JSONResponse(
                    content={"token": token},
                    status_code=200
                )

    raise fastapi.HTTPException(status_code=401, detail="Invalid credentials")
