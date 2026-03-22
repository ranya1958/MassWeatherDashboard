"""
APP/UI Layer
- Side bar with (Params)
    - datepicker for date param
    - radiogroup for snow, precp, avg temp, min temp, max temp
    - dropdown for towns
- Main
    - radio button to choose between tab of weather data or plot
    - data tab has df of current data being visualized as per params set
    - plot tab has geo map visualization as per params set

"""

import panel as pn
import ma_viz as viz
import ma_weather_api as ma_api
import datetime as dt

# DIMENSIONS
CARD_WIDTH = 320
api = None

def prettify(str):
    """Returns a user-friendly version of the string"""
    if str == "PRCP":
        return "Precipitation"
    if str == "SNOW":
        return "Snow"
    if str == "TAVG":
        return "Average Temperature"
    if str == "TMIN":
        return "Minimum Temperature"
    if str == "TMAX":
        return "Maximum Temperature"
    else:
        return str.replace("_", " ").title()

def get_table(date, datatype, town):
    """Returns the table to show in the Table tab."""
    global api
    df = api.get_subset(date=date, town=town, climate_variable=datatype)
    return pn.pane.DataFrame(df)

def get_viz(date, datatype, town, width, height):
    """Returns the plot to show in the Plot tab."""
    global api
    df = api.get_subset(date=date, town=town, climate_variable=datatype)
    fig = viz.plotting(df, datatype, date, town)
    fig.update_layout(width=width, height=height)
    return fig

def main():
    # Loads javascript dependencies and configures Panel (required)
    global api
    pn.extension()

    # Initialize API
    api = ma_api.MAWeatherAPI(ma_api.DATA_FILE_PATH)

    # WIDGET DECLARATIONS
    # Search Widgets

    # date picker for date param
    dates_lst = api.get_dates()
    default_date = dates_lst[0] if len(dates_lst) > 0 else None
    dates_picker = pn.widgets.DatePicker(name='Date', value=default_date,
                                         enabled_dates=dates_lst)

    # add a RadioGroup -- selecting between climate variable types
    climate_vars = api.get_climate_variables()
    pretty_climate_vars = {prettify(var): var
                           for var in climate_vars}
    right_slctr = pn.widgets.RadioButtonGroup(name='Climate Variable',
                                              options=pretty_climate_vars,
                                              value=climate_vars[0] if len(climate_vars) > 0 else None,
                                              button_type="primary",
                                              button_style="outline",
                                              orientation="vertical")

    # add dropdown for town param
    towns_lst = api.get_towns()
    town_slct = pn.widgets.Select(name="Town", options=towns_lst, value=towns_lst[0] if len(towns_lst) > 0 else None)

    # Plotting widgets
    width_sldr = pn.widgets.IntSlider(name="Width", start=800, end=2000, step=100, value=800)
    height_sldr = pn.widgets.IntSlider(name="Height", start=600, end=2000, step=100, value=600)

    # CALLBACK BINDINGS (Connecting widgets to callback functions)
    table = pn.bind(get_table, dates_picker, right_slctr, town_slct)
    plot = pn.bind(get_viz, dates_picker, right_slctr, town_slct, width_sldr, height_sldr)

    # DASHBOARD WIDGET CONTAINERS ("CARDS")
    search_card = pn.Card(
        pn.Column(
            dates_picker, right_slctr, town_slct
        ),
        title="Search", width=CARD_WIDTH, collapsed=False
    )

    plot_card = pn.Card(
        pn.Column(
            width_sldr,
            height_sldr
        ),
        title="Plot", width=CARD_WIDTH, collapsed=True
    )

    # LAYOUT

    layout = pn.template.FastListTemplate(
        title="Massachusetts Weather Dashboard for 2025",
        sidebar=[pn.Column(
            search_card,
            plot_card,
            align="center",
        )],
        theme_toggle=False,
        main=[
            pn.Tabs(
                ("Table", table),
                ("Plot", plot),
                active=1  # Which tab is active by default?
            )
        ],
        header_background='linear-gradient(90deg, #134E5E, #71B280)'

    ).servable()

    layout.show()

if __name__ == "__main__":
    main()