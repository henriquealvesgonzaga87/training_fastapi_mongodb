from pydantic import Field, BaseModel, validator, EmailStr, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Optional
from typing_extensions import Annotated
from datetime import datetime, date
from bson import ObjectId


PyObjectId = Annotated[str, BeforeValidator(str)]


class UserSchema(BaseModel):
    """
    Container for a single user record
    """
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    name: str = Field(...)
    birth_date: str = Field(validator("birth_date", pre=lambda v: datetime.strptime(v, "%Y-%m-%d")))
    email: EmailStr = Field(...)
    password: str = Field()
    cellphone_number: Optional[int] = Field(...)
    model_config = ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_schema_extra={
                "example": {
                    "name": "Jane Doe",
                    "birth_date": "YYYY-mm-dd",
                    "email": "jdoe@example.com",
                    "password": "secret_key",
                    "cellphone_number": "123456789"
                }
            }
        )


class UserSchemaResponse(BaseModel):
    """
    Container for a single user record
    """
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    name: str = Field(...)
    birth_date: date = Field(validator("birth_date", pre=lambda v: datetime.strptime(v, "%Y-%m-%d")))
    email: EmailStr = Field(...)
    cellphone_number: Optional[int] = Field(...)
    model_config = ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_schema_extra={
                "example": {
                    "name": "Jane Doe",
                    "birth_date": "YYYY-mm-dd",
                    "email": "jdoe@example.com",
                    "cellphone_number": "123456789"
                }
            }
        )
