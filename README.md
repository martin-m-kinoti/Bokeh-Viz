# Bokeh Energy Dashboard Backend

This is the **Python/Bokeh backend** for the Energy Consumption Dashboard.  
It serves interactive visualizations of energy consumption in Raven Town using data from CSV files.

## Features

- Processes and merges energy consumption data from multiple CSV files.
- Provides interactive time-series plots with zoom, pan, and hover functionality.
- Supports multiple time resolutions: Raw, Hourly, Daily, Monthly.
- Built using **Bokeh** and **Pandas** for fast, interactive visualizations.

## Access

The backend is deployed and accessible via:  
[https://bokeh-viz.onrender.com](https://bokeh-viz.onrender.com)

## Usage

- The Bokeh server runs the `energy_dashboard.py` script.  
- Make sure the `archive/` folder containing the CSV files is present in the project root.  
- The frontend embeds this backend using an `<iframe>` for visualization.
