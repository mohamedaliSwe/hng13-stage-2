"""Contains the logic for the countries"""

import random
import httpx


COUNT_API = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_RATE_API = "https://open.er-api.com/v6/latest/USD"


async def get_countries():
    """Fetches countries from api"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            country_response = await client.get(COUNT_API)
            country_response.raise_for_status()
            country_data = country_response.json()
            return country_data

    except httpx.HTTPStatusError as e:
        raise Exception(f"Could not fetch data from Countries API: {e}")

    except httpx.RequestError as e:
        raise Exception(f"Countries API request timed out or failed: {e}")


async def get_exchange_rate():
    """Get exchange rate for each country's currency"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            exchange_response = await client.get(EXCHANGE_RATE_API)
            exchange_response.raise_for_status()
            exchange_data = exchange_response.json()
            return exchange_data.get("rates", {})

    except httpx.HTTPStatusError as e:
        raise Exception(f"Could not fetch data from Exchange Rate API: {e}")

    except httpx.RequestError as e:
        raise Exception(f"Exchange Rate API request timed out or failed: {e}")


async def get_country_data():
    """Gets full country data including exchange rate"""
    results = []
    countries = await get_countries()

    has_currency = any(country.get("currencies") for country in countries)
    rates = await get_exchange_rate() if has_currency else None

    for country in countries:
        currencies = country.get("currencies", [])

        if currencies:
            code = currencies[0].get("code")
            exchange_rate = rates.get(code)

            if exchange_rate:
                estimated_gdp = (
                    country.get("population", 0) * random.uniform(1000, 2000)
                ) / exchange_rate
            else:
                estimated_gdp = 0
        else:
            code = None
            exchange_rate = None
            estimated_gdp = 0

        country["currency_code"] = code
        country["exchange_rate"] = exchange_rate
        country["estimated_gdp"] = estimated_gdp

        results.append(country)

    return results
