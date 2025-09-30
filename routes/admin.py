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
    #  TO DO :check admin rights from JWT and verify from DB instead of username
    if payload.get("username") != "admin":
        raise fastapi.HTTPException(status_code=403)

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        raise fastapi.HTTPException(status_code=400)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    async with db.pool.connection() as aconn:
        async with aconn.cursor() as cur:
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
