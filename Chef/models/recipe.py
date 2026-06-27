from pydantic import BaseModel, Field
from typing import Literal, Optional, List


class RecipeAnswer(BaseModel):
    title: str = Field(description="Recipe title")
    ingredients: list[str] = Field(min_length=1)
    steps: list[str] = Field(min_length=1)
    cooking_time_minutes: int = Field(gt=0, le=300)
    difficulty: Literal["easy", "medium", "hard"]
    notes: str | None = None