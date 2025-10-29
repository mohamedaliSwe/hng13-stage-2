"""Contains the Countries model definition"""

import random
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Countries(SQLModel, table=True):
    """Represents a country and its attributes"""

    __tablename__ = "countries"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(nullable=False, index=True)
    capital: Optional[str] = Field(nullable=True)
    region: Optional[str] = Field(nullable=True)
    population: int = Field(nullable=False)
    currency_code: str = Field(nullable=True)
    exchange_rate: float = Field(nullable=True)
    estimated_gdp: Optional[float] = Field(nullable=True)
    flag_url: Optional[str] = Field(nullable=True)
    last_refreshed_at: datetime

    def compute_estimated_gdp(self) -> None:
        """
        Compute and update the estimated GDP.
        """
        self.estimated_gdp = (
            self.population * random.randint(1000, 2000)
        ) / self.exchange_rate
