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
