import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

try:
    df = pd.read_csv('vehicles_us.csv')
except:
    df = pd.read_csv('https://practicum-content.s3.us-west-1.amazonaws.com/datasets/vehicles_us.csv')


st.header('Car Sales Advertisements Project')
st.write('Review Vehicles US dataset to conduct price analysis of used vehicles')

#rename columns to be more descriptive
df.rename(columns={
    'price': 'Price',
    'model_year': 'Model Year',
    'model': 'Car Model',
    'condition': 'Condition',
    'cylinders': 'Cylinders',
    'fuel': 'Fuel Type',
    'odometer': 'Odometer',
    'transmission': 'Transmission Type',
    'type': 'Vehicle Type',
    'paint_color': 'Paint Color',
    'is_4wd': 'is_4WD',
    'date_posted': 'Date Posted',
    'days_listed': 'Days Listed'
}, inplace=True)

#change Date Posted to date type and Model Year to Integer
df['Date Posted'] = pd.to_datetime(df['Date Posted'])
df['Model Year'] = pd.to_datetime(df['Model Year'], format='%Y', errors='coerce')
df['Model Year'] = df['Model Year'].dt.year.astype('Int64')

df['Years Owned'] = df['Date Posted'].dt.year - df['Model Year'] #calculate number of years before sale
valid_model_year = df['Years Owned'].dropna() #drop missing model year
mode_of_year_owned = valid_model_year.mode()[0]

df.loc[df['Model Year'].isna(), 'Model Year'] = df['Date Posted'].dt.year - mode_of_year_owned
# Fill missing 'Model Year' by subtracting the mode from 'Date Posted'

df['Years Owned'] = df['Years Owned'].fillna(5)

for vehicle_type in df['Vehicle Type'].unique():
    mode_value = df[df['Vehicle Type'] == vehicle_type]['Cylinders'].mode().iloc[0]
    df.loc[(df['Vehicle Type'] == vehicle_type) & (df['Cylinders'].isna()), 'Cylinders'] = mode_value


# Fill missing values in 'is_4WD' with the most frequent value for the same 'Car Model'
df['is_4WD'] = df.groupby('Car Model')['is_4WD'].transform('first')

# Replace any remaining NaN values with 'unknown'
df['is_4WD'] = df['is_4WD'].fillna('unknown')


df['Odometer'] = df['Odometer'].fillna(df.groupby(['Model Year', 'Vehicle Type'])['Odometer'].transform('median'))

df['Odometer'] = df['Odometer'].fillna('unknown')

df['Paint Color'] = df['Paint Color'].fillna('unkown')

# Create a new column 'Manufacturer' by extracting the first word from the 'Car Model' column
df['Manufacturer'] = df['Car Model'].str.split().str[0]
# Remove the first word from Car Model
df['Car Model'] = df['Car Model'].str.split().str[1:].str.join(' ')

st.write('### Scatter plot showing Odometer and price model relationship')

Odometer_Price_man = px.scatter(df, x='Odometer', y='Price', color='Car Model', 
                          title='Odometer vs. Price by Car Model', width=900,
height=500)
st.plotly_chart(Odometer_Price_man)

st.write('### Manufacturer Vehicle Type Relationship')
df_histogram_man = px.histogram(data_frame=df, nbins=50, title='Vehicle Type by Manufacturer',
                            x='Manufacturer', color='Vehicle Type', width=900,
height=500)
st.plotly_chart(df_histogram_man)

st.write('### Number of Days Listed per Vehicle Price')

df_histogram = px.histogram(data_frame=df, nbins=50, title='Price of Car and Days Posted',
                            x='Days Listed', color='Vehicle Type', width=900,
height=500)
st.plotly_chart(df_histogram)




st.header("Car Price and Days Listed Histogram")
df_histogram = px.histogram(data_frame=df, nbins=50, title='Price of Car and Days Posted', 
                            x='Days Listed', color='Vehicle Type', width=900, height=500)

# Step 3: Add a checkbox to filter the histogram
filter_days = st.checkbox("Filter vehicles listed for less than 30 Days")

if filter_days:
    # Filter the DataFrame for vehicles listed less than 60 days
    filtered_df = df[df['Days Listed'] < 30]
    df_histogram = px.histogram(data_frame=filtered_df, nbins=50, 
                                title='Price of Car and Days Posted (Listed < 30 Days)', 
                                x='Days Listed', color='Vehicle Type', width=900, height=500)
    st.write(f"Filtered data contains {len(filtered_df)} vehicles.")
else:
    st.write("Displaying all vehicles.")

# Step 4: Display the histogram
st.plotly_chart(df_histogram, key='historgam_all')







