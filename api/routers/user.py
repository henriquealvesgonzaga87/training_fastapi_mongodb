from ..schema import UserSchema
from ..database import client
from ..schema import UserSchema, UserSchemaResponse
from ..utils import hash
from fastapi import APIRouter, status, Body

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
