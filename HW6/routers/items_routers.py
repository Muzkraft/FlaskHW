import logging
from fastapi import APIRouter, HTTPException
from HW6.models.items_model import Item, ItemIn
from HW6.db import database, items

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

item_router = APIRouter()


@item_router.get("/items/", response_model=list[Item])
async def get_items():
    query = items.select()
    return await database.fetch_all(query)


@item_router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    existing_item = await database.fetch_one(query)
    if existing_item:
        return await database.fetch_one(query)
    raise HTTPException(status_code=404, detail="item not found")


@item_router.post("/items/", response_model=Item)
async def create_item(item: ItemIn):
    query = items.insert().values(**item.model_dump())
    last_id = await database.execute(query)
    logger.info(f"Item {item} added")
    return {"id": last_id, **item.model_dump()}


@item_router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, new_item: ItemIn):
    query = items.select().where(items.c.id == item_id)
    existing_item = await database.fetch_one(query)
    if existing_item:
        query = (
            items.update().where(items.c.id == item_id).values(**new_item.model_dump())
        )
        await database.execute(query)
        logger.info(f"Item {item_id} changed")
        return {**new_item.model_dump(), "id": item_id}
    raise HTTPException(status_code=404, detail="Item not found")


@item_router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    existing_item = await database.fetch_one(query)
    if existing_item:
        query = items.delete().where(items.c.id == item_id)
        await database.execute(query)
        logger.info(f"Item {item_id} deleted")
        return {"message": f"Item {item_id} deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
