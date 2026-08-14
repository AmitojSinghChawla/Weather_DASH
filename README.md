# India Weather & Air Quality Dashboard

Real-time weather and air quality monitoring dashboard tracking 5 Indian metros — Delhi, Mumbai, Bangalore, Kolkata, and Chennai.

Built as an end-to-end data engineering + BI project: API ingestion → Cloud PostgreSQL → Automated pipeline → Power BI Dashboard.

## Architecture

```
OpenWeatherMap APIs
    ├── Weather API (v2.5)
    └── Air Pollution API (v2.5)
            │
            ▼
    Python Ingestion Script
    (runs every 15 min via GitHub Actions)
            │
            ▼
    PostgreSQL on Neon (Cloud)
    Star Schema: 4 dimension + 1 fact table
            │
            ▼
    Power BI Dashboard (Import Mode)
    3 pages — Overview, Pollution Deep Dive, Trends
```

## Data Model — Star Schema

| Table | Type | Description |
|-------|------|-------------|
| `locations` | Dimension | 5 Indian metros with coordinates |
| `time` | Dimension | Auto-populated timestamps per ingestion run |
| `pollutants` | Dimension | PM2.5, PM10, NO2, SO2, CO, O3 with safe limits |
| `weather_conditions` | Dimension | Clear, Haze, Rain, Clouds etc. with severity |
| `fact_weather_readings` | Fact | All readings — temp, humidity, wind, pressure, AQI, pollutant concentrations |

Each ingestion run produces 30 rows (5 cities × 6 pollutants), approximately 2,880 rows/day.

## Dashboard Pages

**Page 1 — Live Overview**
- KPI cards: temperature, feels like, humidity, pressure, wind speed, AQI (filtered by city slicer)
- Pollutant concentration vs safe limit comparison
- Current weather condition with icon
- City location map
- All-cities temperature ranking and summary table

**Page 2 — Pollution Deep Dive**
- Pollutant concentration trends over time by city
- Safe limit violation count by pollutant
- Pollution levels by weather condition (donut chart)
- Pollution by time of day — morning, afternoon, night (treemap)
- Wind speed vs pollution correlation (scatter plot)
- City ranking by average pollution

## Key Findings

- **PM2.5 is the primary concern** — highest violation count across all cities
- **Delhi consistently leads** in pollution levels, especially PM2.5 and PM10
- **Rain reduces pollution** — concentration drops during rainy conditions
- **Higher wind speed correlates with lower pollution** — visible downward trend in scatter plot
- **Night pollution is lower** than morning and afternoon, likely due to reduced traffic

## Tech Stack

- **Python** — API calls, data ingestion, DB operations
- **PostgreSQL (Neon)** — Cloud database with star schema
- **psycopg2** — Python-PostgreSQL connector
- **GitHub Actions** — Automated ingestion every 15 minutes
- **Power BI** — Dashboard with DAX measures and interactive slicers
- **OpenWeatherMap API** — Weather and air pollution data source

## Project Structure

```
Weather_DASH/
├── Dashboard/
│   ├── config.py            # DB config and API endpoints
│   ├── db.py                # Database connection and table creation
│   ├── seed.py              # Seed dimension tables with initial data
│   ├── fetch_rawactuals.py  # Main ingestion script
│   └── db_helpers.py        # FK lookup helper functions
├── requirements.txt
├── .github/
│   └── workflows/
│       └── fetch_data.yml   # GitHub Actions automation
└── README.md
```

## Setup

1. Clone the repo
2. Create a Neon PostgreSQL database
3. Add credentials to `.env`:
   ```
   WEATHER_API_KEY=your_openweathermap_key
   DB_HOST=your_neon_host
   DB_NAME=neondb
   DB_USER=neondb_owner
   DB_PASSWORD=your_password
   ```
4. Run `python db.py` to create tables
5. Run `python seed.py` to populate dimension tables
6. Run `python fetch_rawactuals.py` to start collecting data
7. Connect Power BI to your Neon database via PostgreSQL connector

## Automation

GitHub Actions runs the ingestion script every 15 minutes. Secrets are stored in the repository settings. The workflow installs dependencies, sets environment variables, and executes the script.

## Future Improvements

- Add more cities or international locations
- Calculate Indian AQI (0-500 scale) from raw pollutant concentrations
- Deploy on AWS Lambda with CloudWatch triggers
- Add ESP32 sensor for ground-truth comparison
- Add a third dashboard page for historical trends and forecasting
