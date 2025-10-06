import fastapi
import psycopg
#local
import db
import auth 

router = fastapi.APIRouter()

@router.get("/user")
async def hello(
        payload: dict = fastapi.Depends(auth.verify_token)
):
    print("User Connected successfully")
    return {"msg": f"Hello {payload.get('username', 'user')}!"}

@router.get("/user/{user_id}")
    async def get_user(
        user_id: int,
        payload: dict=fastapi.Depends(auth.verify_token)
    ):
    requester_id=payload["sub"]
    role=payload("role","user")
    if requester_id!=user_id and role not in ["sys_admin"]:
        raise fastapi.HTTPException(status_code=403,detail="Forbidden")
    return await db.get_user(user_id)

