import fastapi
#import pydantic
import asyncio
import dotenv
import uvicorn
import datetime

# Local  
import db

load_dotenv()
JWTALGO=os.getenv("JWTALGO")
JWTSECRETKEY=os.getenv("JWTSECRETKEY")
app=FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await pool.close()

app.include_router(login.router)
app.include_router(user.router)
app.include_router(admin.router)
