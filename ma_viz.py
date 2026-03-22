
"""
Daily climate data of Massachusetts in 2025
Map visualization of Massachusetts with Params:
    - Date DDMMYY
    - Data type (climate variable) color scale - prcp, snow, avg temp, max/min temp
    - town
    on hover: station name, datatype value
    title: {datatype} data on {date} in Massachusetts
"""
import plotly.graph_objects as go
import pandas as pd
import ma_weather_app as app
from ma_weather_app import prettify

colors = {
    "PRCP": "blugrn",
    "SNOW": "ice",
    "TAVG": "jet",
    "TMIN": "sunsetdark",
    "TMAX": "blured"
}

def plotting(df, datatype, date, town="All Towns"):
    """
    Plot stations in Massachusetts for the given
    date + datatype (e.g. PRCP, SNOW), colored by value.
    """

    if date is not None and "date" in df.columns:
        df = df[df["date"] == date]

    if datatype is not None and "datatype" in df.columns:
        df = df[df["datatype"] == datatype]

    if town is not None and town != "All Towns" and "town" in df.columns:
        df = df[df["town"] == town]

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=None,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[
                dict(
                    text="No data available for this selection",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=18),
                )
            ],
        )
        return fig

    # hover
    df = df.copy()
    df["hover"] = (
        df["name"].astype(str)
        + "<br>"
        + datatype
        + ": "
        + df["value"].astype(str)
    )

    values = df["value"].astype(float)
    colorscale = colors.get(datatype, "Viridis")
    fig = go.Figure(
        go.Scattergeo(
            locationmode="USA-states",
            lon=df["longitude"],
            lat=df["latitude"],
            text=df["hover"],
            mode="markers",
            marker=dict(
                size=8,
                opacity=0.8,
                symbol="circle",
                color=values,
                colorscale=colorscale,
                colorbar=dict(title=app.prettify(datatype)),
            ),
        )
    )

    title = f"{app.prettify(datatype)} on {date}"
    if town is not None and town != "All Towns":
        title += f" in {town}"

    fig.update_layout(
        title=title,
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            center=dict(lat=42.3, lon=-71.8),  # center roughly on MA
            projection_scale=6,
            showland=True,
            landcolor="rgb(250, 250, 250)",
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)",
            countrywidth=0.5,
            subunitwidth=0.5,
        ),
        height=520,
        margin=dict(l=0, r=0, t=45, b=0),
    )

    return fig