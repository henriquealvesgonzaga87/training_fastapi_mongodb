from ..schema import UserSchema
from ..database import client
from ..schema import UserSchema, UserSchemaResponse, UserCollectionResponse
from ..utils import hash
from fastapi import APIRouter, status, Body, HTTPException
from fastapi.responses import Response
from bson import ObjectId
from pymongo import ReturnDocument


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

db = client.get_database("user")
user_collection = db.get_collection("user")

@router.post("/user_create/", response_model=UserSchemaResponse, status_code=status.HTTP_201_CREATED)
async def creat_user(user: UserSchema = Body(...)):
    """
    Insert a new user record.

    A unique `id` will be created and provided in the response.
    """
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = user_collection.insert_one(user.model_dump(by_alias=True, exclude=["id"]))
    created_user = user_collection.find_one({"_id": new_user.inserted_id})
    return created_user


@router.put("/user_update/{id}", response_model=UserSchemaResponse, status_code=status.HTTP_200_OK)
async def update_user(id: str, user: UserSchema = Body(...)):
    """
    Update individual fields of an existing user record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """

    hashed_password = hash(user.password)
    user.password = hashed_password

    user = {k: v for k, v in user.model_dump(by_alias=True).items() if v is not None}

    if len(user) >= 1:
        update_result = user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := user_collection.find_one({"_id":id})) is not None:
        return existing_user
    
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.get("/list_user/{id}", response_model=UserSchemaResponse, response_model_by_alias=False, status_code=status.HTTP_200_OK)
async def list_one_user(id: str):
    """
    search for one user in the database by their id
    """

    result = user_collection.find_one({"_id": ObjectId(id)})
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.get("/all_users/", response_model=UserCollectionResponse, response_model_by_alias=False, status_code=status.HTTP_200_OK)
async def list_all_users():
    """
    List all users from the database
    """
    return UserCollectionResponse(users=user_collection.find())


@router.delete("/delete/{id}")
async def delete_user(id: str):
    
    filter = user_collection.delete_one({"_id": ObjectId(id)})

    if filter.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"User {id} not found!")
