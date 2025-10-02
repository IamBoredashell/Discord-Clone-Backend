
import fastapi
import bcrypt
#local
import db
import auth

router = fastapi.APIRouter()

@router.get("/user/get_info")
async def get_info(
        data: dict = fastapi.Body(...),
        payload: dict = fastapi.Depends(auth.verify_token)
):
    pass 

