import os
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import column
from bokeh.io import curdoc

# Resolve data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "archive")

# Load data
jan_first = pd.read_csv(os.path.join(DATA_DIR, "KwhConsumptionBlower78_1.csv"))
jan_second = pd.read_csv(os.path.join(DATA_DIR, "KwhConsumptionBlower78_2.csv"))
feb = pd.read_csv(os.path.join(DATA_DIR, "KwhConsumptionBlower78_3.csv"))

# Merge and clean data
df = pd.concat([jan_first, jan_second, feb]).drop_duplicates()

df["Datetime"] = pd.to_datetime(
    df["TxnDate"] + " " + df["TxnTime"],
    format="%d %b %Y %H:%M:%S"
)

df = (
    df.set_index("Datetime")
      .sort_index()
      .drop(columns=["TxnDate", "TxnTime"])
)

df.index = df.index.tz_localize("Africa/Nairobi").tz_convert(None)

# Prepare aggregated views
data_views = {
    "Raw": df.reset_index(),
    "Hourly": df.resample("H").sum().reset_index(),
    "Daily": df.resample("D").sum().reset_index(),
    "Monthly": df.resample("M").sum().reset_index(),
}

# Create data source
source = ColumnDataSource(data_views["Raw"].to_dict("list"))

# Build plot
p = figure(
    x_axis_type="datetime",
    title="Energy Consumption Over Time",
    width=900,
    height=420,
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

p.line(
    x="Datetime",
    y="Consumption",
    source=source,
    line_width=2
)

p.xaxis.axis_label = "Time"
p.yaxis.axis_label = "Consumption (kWh)"

hover = HoverTool(
    tooltips=[
        ("Time", "@Datetime{%F %T}"),
        ("Consumption", "@Consumption{0.000} kWh"),
    ],
    formatters={"@Datetime": "datetime"},
)

p.add_tools(hover)

# Add selector logic
select = Select(
    title="Time Resolution",
    value="Raw",
    options=list(data_views.keys())
)

def update(attr, old, new):
    new_df = data_views[new]
    source.data = new_df.to_dict("list")
    p.y_range.start = new_df["Consumption"].min() * 0.9
    p.y_range.end = new_df["Consumption"].max() * 1.1

select.on_change("value", update)

# Layout and serve
curdoc().add_root(column(select, p))
curdoc().title = "Energy Consumption Dashboard"
