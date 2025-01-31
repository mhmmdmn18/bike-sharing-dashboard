import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset
df = pd.read_csv("hour_df.csv")
df['dteday'] = pd.to_datetime(df['dteday'])
df.set_index('dteday', inplace=True)

# Sidebar filters
with st.sidebar:
    start_date, end_date = st.date_input("Rentang Waktu", [df.index.min(), df.index.max()], min_value=df.index.min(), max_value=df.index.max())

# Filter data
main_df = df.loc[start_date:end_date]

# Header
st.header('Bike Rental Dashboard 🚴‍♂️📊')

# Metrics
col1, col2 = st.columns(2)
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Rentals", value=total_rentals)
with col2:
    avg_temp = round(main_df['temp'].mean(), 2)
    st.metric("Average Temperature", value=f"{avg_temp} °C")

# Daily Rentals Trend
st.subheader("Daily Rentals Trend")
daily_rentals = main_df.resample('D').sum()['cnt']
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_rentals.index, daily_rentals, marker='o', color='#90CAF9', linewidth=2)
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Rentals by Weather Condition
st.subheader("Impact of Weather on Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=main_df, ax=ax, palette='coolwarm')
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Bike Rentals")
st.pyplot(fig)

# Rentals by Hour
st.subheader("Hourly Rental Patterns")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=main_df, ci=None, marker='o')
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Casual vs Registered Rentals
st.subheader("Casual vs Registered Users")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='casual', data=main_df, label='Casual', ci=None)
sns.lineplot(x='hr', y='registered', data=main_df, label='Registered', ci=None)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Number of Rentals")
ax.legend()
st.pyplot(fig)

st.caption('Copyright © Muhammad Aminuddin 2025')
