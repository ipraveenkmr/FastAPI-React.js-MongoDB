from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import collections
from bson.objectid import ObjectId
from app.utils import serialize_document

router = APIRouter()

# MongoDB collection for items
items_collection = collections["items"]


# Pydantic model for item
class Item(BaseModel):
    name: str


# Create an item
@router.post("/items", status_code=201)
async def create_item(item: Item):
    if not item.name:
        raise HTTPException(status_code=400, detail="Name is required")
    
    try:
        new_item = {"name": item.name}
        result = items_collection.insert_one(new_item)
        return {"id": str(result.inserted_id), "name": item.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


# Retrieve all items
@router.get("/items")
async def get_items():
    try:
        items = list(items_collection.find())
        return [serialize_document(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


# Retrieve a specific item by ID
@router.get("/items/{item_id}")
async def get_item(item_id: str):
    try:
        item = items_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return serialize_document(item)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid ID format or database error")


# Update an item by ID
@router.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    if not item.name:
        raise HTTPException(status_code=400, detail="Name is required")
    
    try:
        result = items_collection.update_one(
            {"_id": ObjectId(item_id)}, {"$set": {"name": item.name}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": item_id, "name": item.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid ID format or database error")


# Delete an item by ID
@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str):
    try:
        result = items_collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid ID format or database error")
