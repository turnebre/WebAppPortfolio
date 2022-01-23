from cProfile import run
from email import message
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, date, timedelta, time as dtime
import time
from gspread_pandas import Spread


def make_covid_dashboard():
    def load_data():
        loading = st.info("Loading data from source")
        covid_data_raw = pd.read_csv(
            "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
            parse_dates=["date"],
        )

        loading.empty()

        return covid_data_raw

    def clean_data(raw_data: pd.DataFrame()):
        """
        Cleans data by removing uneeded columns and dropping continents.
        Also interpolates vaccination data due to inconsitencies each day.
        """
        cleaning = st.info("Cleaning data")
        covid_data_raw = raw_data.loc[~raw_data["continent"].isna(), :]

        regex = """total|excess|aged|extreme|capita|cardiovasc|\
            |smokers|tests|index|expectancy|beds|density|\
                |handwashing|diabetes|median|positive|reproduction|\
                    |iso_code|continent|weekly|per_million|per_hundred|smoothed"""

        dropped_columns = list(covid_data_raw.filter(regex=regex))

        booster_column = ["total_boosters"]

        covid_data = covid_data_raw.copy()[covid_data_raw.columns.drop(dropped_columns)]

        covid_data[booster_column] = covid_data_raw[booster_column]

        interp_columns = [
            "people_fully_vaccinated",
            "people_vaccinated",
            "total_boosters",
        ]

        covid_data_interp = pd.DataFrame()

        locations = covid_data["location"].unique()

        for location in locations:
            location_set = covid_data.copy().loc[covid_data["location"] == location, :]
            location_set = location_set.sort_values(["location", "date"])
            location_set[interp_columns] = location_set[interp_columns].interpolate()
            location_set.iloc[:, 2:] = location_set.iloc[:, 2:].fillna(0)
            covid_data_interp = covid_data_interp.copy().append(location_set)

        cleaning.empty()

        return covid_data_interp

    def export_data(cleaned_data: pd.DataFrame()):
        """
        Uploads data to Google Sheets and schedules the next run for 4pm the following day.
        """
        exporting = st.info("Exporting to Google Sheets")

        spread = Spread("COVID Dashboard")
        spread.df_to_sheet(
            cleaned_data, index=False, sheet="Dashboard Data", start="A1", replace=True,
        )
        exporting.empty()

    dashboard = components.html(
        """
            <div class='tableauPlaceholder' id='viz1642887830638' style='position: relative'><object class='tableauViz'
            style='display:none;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='COVIDDashboard_16406598287530&#47;COVIDDashboard' />
            <param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
            <param name='filter' value='publish=yes' />
        </object></div>
    <script type='text/javascript'>
        var divElement = document.getElementById('viz1642887830638');
        var vizElement = divElement.getElementsByTagName('object')[0];
        vizElement.style.width = '100%';
        vizElement.style.height = '800px';
        var scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """,
        height=800,
    )

    if datetime.now().time() >= dtime(9, 30):
        run_date = datetime.now().date() + timedelta(days=1)
        runtime = datetime.combine(run_date, dtime(9, 30))
        print("Next Runtime: " + str(runtime))
    else:
        runtime = datetime.combine(datetime.now().date(), dtime(9, 30))
        print("Next Runtime: " + str(runtime))

    now = datetime.now()
    if now >= runtime:
        dashboard.empty()
        progress = 0
        my_bar = st.progress(progress)

        raw_data = load_data()
        progress += 1 / 3
        my_bar.progress(progress)

        cleaned_data = clean_data(raw_data)
        progress += 1 / 3
        my_bar.progress(progress)

        export_data(cleaned_data)
        progress += 1 / 3
        my_bar.progress(progress)

        success = st.success("Successfully exported data")
        time.sleep(3)
        success.empty()
        my_bar.empty()
        dashboard
