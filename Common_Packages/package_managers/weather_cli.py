# package_managers/weather_cli.py
from __future__ import annotations
import sys
from typing import Tuple, Optional
import requests
import typer
from rich import print
from rich.table import Table

app = typer.Typer(add_completion=False, help="Weather CLI (Open-Meteo)")

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def geocode(city: str) -> Tuple[float, float, str]:
    """Zwraca (lat, lon, resolved_name) dla podanego miasta."""
    r = requests.get(GEOCODE_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        typer.secho(f"City not found: {city}", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)
    item = results[0]
    name = f'{item["name"]}, {item.get("country_code","")}'
    return float(item["latitude"]), float(item["longitude"]), name

@app.command()
def now(city: str = typer.Argument(..., help="City name, e.g. 'Warsaw'")):
    """Pokaż bieżącą pogodę."""
    lat, lon, name = geocode(city)
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
        "timezone": "auto",
    }
    r = requests.get(FORECAST_URL, params=params, timeout=10)
    r.raise_for_status()
    cur = r.json().get("current") or {}
    table = Table(title=f"Current weather — {name}")
    table.add_column("Metric"); table.add_column("Value")
    table.add_row("Temperature", f'{cur.get("temperature_2m","?")} °C')
    table.add_row("Wind", f'{cur.get("wind_speed_10m","?")} km/h')
    table.add_row("Humidity", f'{cur.get("relative_humidity_2m","?")} %')
    print(table)

@app.command()
def forecast(
    city: str = typer.Argument(..., help="City name, e.g. 'Warsaw'"),
    days: int = typer.Option(3, min=1, max=14, help="How many days (1–14)"),
):
    """Pokaż prognozę dzienną na N dni."""
    lat, lon, name = geocode(city)
    params = {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": days,
    }
    r = requests.get(FORECAST_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json().get("daily") or {}

    dates = data.get("time", [])
    tmax = data.get("temperature_2m_max", [])
    tmin = data.get("temperature_2m_min", [])
    rain = data.get("precipitation_sum", [])

    table = Table(title=f"Forecast — {name} (next {days} day(s))")
    for col in ("Date", "Min °C", "Max °C", "Rain mm"):
        table.add_column(col)
    for d, lo, hi, rr in zip(dates, tmin, tmax, rain):
        table.add_row(d, f"{lo:.1f}", f"{hi:.1f}", f"{rr:.1f}")
    print(table)

if __name__ == "__main__":
    try:
        app()
    except requests.RequestException as e:
        typer.secho(f"Network error: {e}", err=True, fg=typer.colors.RED)
        sys.exit(2)
