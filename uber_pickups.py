import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')
 
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
 
@st.cache_data #โหลดแค่ครั้งเดียว
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
 
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
 
#data
st.subheader("Raw Data")
st.write(data)
 
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour,bins=24,range=(0,24))[0]
 
st.bar_chart(hist_values)
st.subheader('Map of all pickups')
st.map(data)
 
#hour_to_filter = 1
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
 
 
 
 
####################  3D pydeck ##########################
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
 
chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

 
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=chart_data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)
 

# ======= Widgets: Date & Hour Selection =======
unique_dates = pd.to_datetime(data['date/time'].dt.date.unique())
selected_date = st.date_input("📅 Select a Date", value=unique_dates[0])
hour_selected = st.selectbox("⏰ Select Hour", options=list(range(24)), index=17)

# ======= Filtered Data =======
filtered = data[data['date/time'].dt.date == selected_date]
filtered = filtered[filtered['date/time'].dt.hour == hour_selected]

# ======= Plotly Chart =======
import plotly.express as px 
st.subheader(f'📊 Number of pickups per hour on {selected_date}')
hourly_counts = data[data['date/time'].dt.date == selected_date].copy()
hourly_counts['hour'] = hourly_counts['date/time'].dt.hour
fig = px.histogram(hourly_counts, x='hour', nbins=24, title='Pickups per Hour', labels={'hour': 'Hour of Day'})
st.plotly_chart(fig, use_container_width=True)

# ======= 3D Map using pydeck =======
st.subheader(f'🌐 3D Map of pickups at {hour_selected}:00 on {selected_date}')
if not filtered.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(
            latitude=filtered['lat'].mean(),
            longitude=filtered['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=filtered,
                get_position='[lon, lat]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=80,
            ),
        ]
    ))
else:
    st.warning("No data available for this hour and date.")


##################### Run X times ######################
import streamlit as st
 
if "counter" not in st.session_state:
    st.session_state.counter = 0
 
st.session_state.counter += 1
 
st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")