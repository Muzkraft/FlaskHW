from fastapi import APIRouter, HTTPException
from HW6.db import users, database
from HW6.models.users_model import User, UserIn

user_router = APIRouter()


@user_router.get('/users/', response_model=list[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@user_router.post('/users/', response_model=UserIn)
async def create_user(user: UserIn):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), 'user_id': last_record_id}


@user_router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    result = await database.fetch_one(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail='User not found')


@user_router.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.user_id == user_id).values(**new_user.dict())
    result = await database.execute(query)
    if result:
        return {**new_user.dict(), 'user_id': user_id}
    raise HTTPException(status_code=404, detail='User not found')


@user_router.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    result = await database.execute(query)
    if result:
        return {'message': f"User {user_id} deleted"}
    raise HTTPException(status_code=404, detail='User not found')

