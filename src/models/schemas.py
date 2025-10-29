"""Contains pydantic schemas for coutries"""

from pydantic import BaseModel
from typing import Optional


class CountriesResponseModel(BaseModel):
    """Countries response model"""

    id: str
    name: str
    capital: Optional[str] | None = None
    region: Optional[str] | None = None
    population: int | None = None
    currency_code: str | None = None
    exchange_rate: float | None = None
    estimated_gdp: Optional[float] | None = None
    flag_url: Optional[str] | None = None
    last_refreshed_at: str


class StatusResponseModel(BaseModel):
    """Status response model"""

    total_countries: int
    last_refreshed_at: str
