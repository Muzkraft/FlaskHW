from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from routers.users_routers import user_router
from routers.items_routers import item_router
from routers.orders_routers import order_router
from db import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, tags=["users"])
app.include_router(item_router, tags=["items"])
app.include_router(order_router, tags=["orders"])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
