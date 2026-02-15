from typing import Optional

from pydantic import BaseModel, Field


class AdvertisementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    description: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1, max_length=256)


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = Field(None, min_length=1)
    owner: Optional[str] = Field(None, min_length=1, max_length=256)
