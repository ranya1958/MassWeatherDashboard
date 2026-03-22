"""
API Layer - Data loading, processing, and filtering
"""
import pandas as pd

# Constants
DATA_FILE_PATH = "ma_data.csv"
CLIMATE_VAR_TYPE = "datatype"
STATION_ID = "station_id"
STATION_NAME = "name"
CLIMATE_VAR_VALUE = "value"
LATITUDE = "latitude"
LONGITUDE = "longitude"
TOWN = "town"
DATE = "date"

class MAWeatherAPI:
    def __init__(self, filename):
        """Load data from csv file"""
        self._raw_df = pd.read_csv(filename)
        self.df = self.process_data(self._raw_df)

    def process_data(self, df):
        """
        Clean data, handle missing values
        IMPORTANT: UI calls api.process_data() with no args, so df is optional.
        """
        if df is None:
            df = self._raw_df
        critical_cols = [DATE, CLIMATE_VAR_TYPE, STATION_ID, STATION_NAME, CLIMATE_VAR_VALUE, LATITUDE, LONGITUDE]
        df_cleaned = df[critical_cols].copy()
        df_cleaned[DATE] = pd.to_datetime(df_cleaned[DATE]).dt.date
        df_cleaned = df_cleaned[
            df_cleaned[CLIMATE_VAR_TYPE].isin(["PRCP", "SNOW", "TAVG", "TMIN", "TMAX"])]
        df_cleaned[TOWN] = (df_cleaned[STATION_NAME].astype(str).str.split().str[0])
        df_cleaned = df_cleaned.dropna(subset=critical_cols)
        self.df = df_cleaned
        return df_cleaned

    def get_dates(self):
        """Return list of dates for datepicker"""
        dates = sorted(
            self.df[DATE]
            .dropna()
            .unique()
            .tolist()
        )
        return dates

    def get_towns(self):
        """Return list of towns for dropdown"""
        towns = sorted(
            self.df[TOWN]
            .dropna()
            .unique()
            .tolist()
        )
        return ["All Towns"] + towns

    def get_climate_variables(self):
        """Return list of climate variables for radiobuttons"""
        climate_variables = sorted(
            self.df[CLIMATE_VAR_TYPE]
            .dropna()
            .unique()
            .tolist()
        )
        return climate_variables

    def get_subset(self, date=None, town=None, climate_variable=None):
        df = self.df

        if date is not None:
            df = df[df["date"] == date]

        if town is not None and town != "All Towns":
            df = df[df["town"] == town]

        if climate_variable is not None:
            df = df[df["datatype"] == climate_variable]

        return df

def main():
    api = MAWeatherAPI(DATA_FILE_PATH)

if __name__ == "__main__":
    main()
