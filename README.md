# Country Currency & Exchange API

A  RESTful API that fetches country data from an external API, stores it in a database, and provides CRUD operations.

## Features

- Fetch country data from: https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
- For each country, extract the currency code (e.g. NGN, USD, GBP).
- Then fetch the exchange rate from: https://open.er-api.com/v6/latest/USD
- Match each country's currency with its rate (e.g. NGN → 1600).
- Compute a field estimated_gdp = population × random(1000–2000) ÷ exchange_rate.
- Store or update everything in MySQL as cached data.
- JSON-based responses with clear documentation via Swagger UI (`/docs`)

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** MySQL

## Set Up

1. Clone the Repository

```bash
git clone https://github.com/<your-username>/countries.git
cd countries
```

2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Configure Environment Variables

```.env
DB_URL
```

5. Run the Application

```bash
fastapi dev src.app.py
```

6. Open your browser and visit [http://127.0.0.1:8000/docs]. You should see the Swagger UI to test the api.

## Response Example

```bash
[
  {
    "id": "002e57ec-ed80-46dc-9329-56d812b3dd68",
    "name": "Saint Helena, Ascension and Tristan da Cunha",
    "capital": "Jamestown",
    "region": "Africa",
    "population": 4255,
    "currency_code": "SHP",
    "exchange_rate": 0.752888,
    "estimated_gdp": 6247110,
    "flag_url": "https://flagcdn.com/sh.svg",
    "last_refreshed_at": "2025-10-29T19:00:15Z"
  },
  {
    "id": "0031fd88-dcbd-41e1-9056-63ae3c4851b1",
    "name": "Tuvalu",
    "capital": "Funafuti",
    "region": "Oceania",
    "population": 11792,
    "currency_code": "AUD",
    "exchange_rate": 1.52189,
    "estimated_gdp": 12617800,
    "flag_url": "https://flagcdn.com/tv.svg",
    "last_refreshed_at": "2025-10-29T18:24:56Z"
  }
]
```

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, under the conditions of the MIT License.