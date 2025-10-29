"""Contains the countries API endpoint"""

import datetime
import os
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from sqlmodel import select, col
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.db import get_session
from src.models.country import Countries
from src.models.schemas import CountriesResponseModel, StatusResponseModel
from src.services.summary import generate_summary_image
from src.services.countries import get_country_data


router = APIRouter(tags=["Countries"])


@router.get("/countries", response_model=list[CountriesResponseModel])
async def get_all_countries(
    db: AsyncSession = Depends(get_session),
    region: Optional[str] = Query(None),
    currency: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
):
    """Fetches all countries from DB"""

    query = select(Countries)

    if region:
        query = query.where(col(Countries.region).ilike(f"%{region}%"))

    if currency:
        query = query.where(col(Countries.currency_code) == currency.upper())

    if sort:
        if sort == "gdp_desc":
            query = query.order_by(Countries.estimated_gdp.desc())
        elif sort == "gdp_asc":
            query = query.order_by(Countries.estimated_gdp.asc())
        elif sort == "population_desc":
            query = query.order_by(Countries.population.desc())
        elif sort == "population_asc":
            query = query.order_by(Countries.population.asc())
        elif sort == "name_desc":
            query = query.order_by(Countries.name.desc())
        elif sort == "name_asc":
            query = query.order_by(Countries.name.asc())

    result = await db.exec(query)
    countries = result.all()

    return [
        CountriesResponseModel(
            id=str(c.id),
            name=c.name,
            capital=c.capital,
            region=c.region,
            population=c.population,
            currency_code=c.currency_code,
            exchange_rate=c.exchange_rate,
            estimated_gdp=c.estimated_gdp,
            flag_url=c.flag_url,
            last_refreshed_at=(
                c.last_refreshed_at.isoformat() + "Z" if c.last_refreshed_at else None
            ),
        )
        for c in countries
    ]


@router.post("/countries/refresh", response_model=list[CountriesResponseModel])
async def fetch_all_countries(db: AsyncSession = Depends(get_session)):
    """Fetch all the countries"""
    data = await get_country_data()

    result = await db.exec(select(Countries))
    existing_countries = result.all()

    existing_countries_map = {
        country.name.lower(): country for country in existing_countries
    }

    for c in data:
        country_name = c.get("name")
        country_name_lower = country_name.lower() if country_name else ""

        if country_name_lower in existing_countries_map:
            existing_country = existing_countries_map[country_name_lower]
            existing_country.name = c.get("name")
            existing_country.capital = c.get("capital")
            existing_country.region = c.get("region")
            existing_country.population = c.get("population")
            existing_country.currency_code = c.get("currency_code")
            existing_country.exchange_rate = c.get("exchange_rate")
            existing_country.estimated_gdp = c.get("estimated_gdp")
            existing_country.flag_url = c.get("flag")
            existing_country.last_refreshed_at = datetime.datetime.utcnow()

            db.add(existing_country)
        else:
            country = Countries(
                name=c.get("name"),
                capital=c.get("capital"),
                region=c.get("region"),
                population=c.get("population"),
                currency_code=c.get("currency_code"),
                exchange_rate=c.get("exchange_rate"),
                estimated_gdp=c.get("estimated_gdp"),
                flag_url=c.get("flag"),
                last_refreshed_at=datetime.datetime.utcnow(),
            )
            db.add(country)

    await db.commit()

    result = await db.exec(select(Countries))
    countries = result.all()

    top_countries_query = (
        select(Countries).order_by(Countries.estimated_gdp.desc()).limit(5)
    )
    top_result = await db.exec(top_countries_query)
    top_countries = top_result.all()

    top_countries_data = [
        {"name": c.name, "estimated_gdp": c.estimated_gdp or 0} for c in top_countries
    ]

    generate_summary_image(
        total_countries=len(countries),
        top_countries=top_countries_data,
        last_refresh=datetime.datetime.utcnow().isoformat() + "Z",
        output_path="cache/summary.png",
    )

    return [
        CountriesResponseModel(
            id=str(c.id),
            name=c.name,
            capital=c.capital,
            region=c.region,
            population=c.population,
            currency_code=c.currency_code,
            exchange_rate=c.exchange_rate,
            estimated_gdp=c.estimated_gdp,
            flag_url=c.flag_url,
            last_refreshed_at=(
                c.last_refreshed_at.isoformat() + "Z" if c.last_refreshed_at else None
            ),
        )
        for c in countries
    ]


@router.get("/countries/image")
async def get_countries_image():
    """Serve summary image"""
    image_path = "cache/summary.png"

    if not os.path.exists(image_path):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Image not found",
                "message": "No summary image available. Please refresh country data first by calling POST /countries/refresh",
            },
        )

    return FileResponse(
        image_path,
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=summary.png"},
    )


@router.get("/countries/{name}", response_model=CountriesResponseModel)
async def get_country_by_name(name: str, db: AsyncSession = Depends(get_session)):
    """Get one country by name (case-insensitive)"""
    query = select(Countries).where(col(Countries.name).ilike(name))
    result = await db.exec(query)
    country = result.first()

    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Country '{name}' not found"
        )

    return CountriesResponseModel(
        id=str(country.id),
        name=country.name,
        capital=country.capital,
        region=country.region,
        population=country.population,
        currency_code=country.currency_code,
        exchange_rate=country.exchange_rate,
        estimated_gdp=country.estimated_gdp,
        flag_url=country.flag_url,
        last_refreshed_at=(
            country.last_refreshed_at.isoformat() + "Z"
            if country.last_refreshed_at
            else None
        ),
    )


@router.delete("/countries/{name}")
async def delete_country_by_name(name: str, db: AsyncSession = Depends(get_session)):
    """Delete a country by name"""
    query = select(Countries).where(col(Countries.name).ilike(name))
    result = await db.exec(query)
    country = result.first()

    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Country '{name}' not found"
        )

    await db.delete(country)
    await db.commit()


@router.get("/status", response_model=StatusResponseModel)
async def get_status(db: AsyncSession = Depends(get_session)):
    """Show total countries and last refresh timestamp"""

    query = select(Countries)
    result = await db.exec(query)
    countries = result.all()

    total_countries = len(countries)

    last_refresh = None
    if countries:
        last_refresh = max(
            (c.last_refreshed_at for c in countries if c.last_refreshed_at),
            default=None,
        )

    return StatusResponseModel(
        total_countries=total_countries,
        last_refreshed_at=last_refresh.isoformat() + "Z",
    )
