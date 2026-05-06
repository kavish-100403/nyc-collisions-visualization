# NYC Traffic Collision Dashboard

Interactive dashboard for exploring NYC motor vehicle collisions: spatial hotspots, top reported contributing factors, monthly trends, and summary KPIs. Built with **Python**, **Pandas**, **Plotly**, and **Dash**.

## Prerequisites

- **Python 3.9+**
- NYC Open Data crash CSV (see [Data](#data))

## Dependencies

Install from the project root:

```bash
python -m venv venv
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Packages: `pandas`, `plotly`, `dash` (see `requirements.txt`).

## Data

The app reads **`data/processed/collisions_cleaned.csv`**.

1. Download the dataset **Motor Vehicle Collisions – Crashes** from [NYC Open Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95).
2. Save the CSV as:

   `data/raw/Motor_Vehicle_Collisions.csv`

3. Generate the cleaned file:

   ```bash
   python src/clean_data.py
   ```

   This writes `data/processed/collisions_cleaned.csv` (and a small sample under `data/sample/`).

If you already have `collisions_cleaned.csv` in `data/processed/`, you can skip steps 1–3 and run the app directly.

## How to run the dashboard

From the **project root** (same folder as `app.py`), with your virtual environment activated:

```bash
python app.py
```

Open a browser at **http://127.0.0.1:8050/**. Stop the server with `Ctrl+C`.

- **Year / Borough / Time of day** filters update the map, charts, and summary cards together.
- The map uses crashes with **3+ injuries or any fatality** for the density layer.

## Example usage

- Pick **2026** and **All Boroughs** to see citywide patterns for the latest year in the cleaned data.
- Choose **Brooklyn** and **Afternoon** to compare subset counts with the summary cards and monthly trend.
- Use the **contributing factors** bar chart to see the most frequent *reported* factor for vehicle.

## Project layout

| Path | Purpose |
|------|---------|
| `app.py` | Dash app: layout, filters, charts, callbacks |
| `src/clean_data.py` | Raw CSV → cleaned CSV |
| `data/raw/` | Place downloaded NYC CSV here |
| `data/processed/` | Output of `clean_data.py` (used by the app) |
| `requirements.txt` | Python dependencies |

## Troubleshooting

- **`FileNotFoundError` for `collisions_cleaned.csv`:** Run `python src/clean_data.py` after placing the raw CSV in `data/raw/`.
- **Port in use:** Another process may be using `8050`. Close it or set a port in `app.py`, e.g. `app.run(debug=True, port=8051)`.
