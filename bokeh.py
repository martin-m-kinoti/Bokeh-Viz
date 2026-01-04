# Libraries
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import column
from bokeh.io import curdoc

# Load data
jan_first = pd.read_csv(r"archive\KwhConsumptionBlower78_1.csv")
jan_second = pd.read_csv(r"archive\KwhConsumptionBlower78_2.csv")
feb = pd.read_csv(r"archive\KwhConsumptionBlower78_3.csv")

# Merge and clean
df = pd.concat([jan_first, jan_second, feb]).drop_duplicates()

# Datetime processing
df["Datetime"] = pd.to_datetime(
    df["TxnDate"] + " " + df["TxnTime"],
    format="%d %b %Y %H:%M:%S"
)

df = (
    df.set_index("Datetime")
      .sort_index()
      .drop(columns=["TxnDate", "TxnTime"])
)

# Localize (Kenya) then REMOVE timezone for Bokeh
df.index = df.index.tz_localize("Africa/Nairobi").tz_convert(None)

# Precompute aggregations
data_views = {
    "Raw": df.reset_index(),
    "Hourly": df.resample("H").sum().reset_index(),
    "Daily": df.resample("D").sum().reset_index(),
    "Monthly": df.resample("M").sum().reset_index(),
}

# Single ColumnDataSource (CRITICAL)
source = ColumnDataSource(data_views["Raw"].to_dict("list"))

# Plot
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

# Hover tool
hover = HoverTool(
    tooltips=[
        ("Time", "@Datetime{%F %T}"),
        ("Consumption", "@Consumption{0.000} kWh"),
    ],
    formatters={"@Datetime": "datetime"},
)

p.add_tools(hover)

# Dropdown selector
select = Select(
    title="Time Resolution",
    value="Raw",
    options=list(data_views.keys())
)

def update(attr, old, new):
    new_df = data_views[new]

    # Update data
    source.data = new_df.to_dict("list")

    # Auto-scale y-axis
    p.y_range.start = new_df["Consumption"].min() * 0.9
    p.y_range.end = new_df["Consumption"].max() * 1.1

select.on_change("value", update)

# Layout
layout = column(select, p)

# Add to Bokeh document
curdoc().add_root(layout)
curdoc().title = "Energy Consumption Dashboard"
