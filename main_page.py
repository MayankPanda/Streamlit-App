import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_file = './data.csv'
df = pd.read_csv(csv_file)
print(list(df.columns.values))

# Function to read the Backlog value from the variable.txt file
def read_backlog():
    try:
        with open('variable.txt', 'r') as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return 0

# Function to write the Backlog value to the variable.txt file
def write_backlog(value):
    with open('variable.txt', 'w') as file:
        file.write(str(value))

# Initialize Backlog
backlog = read_backlog()
# Function to add a new record
@st.dialog("Add a Record")
def add_record():
    global backlog
    st.write("Add a new record")
    date = st.date_input("Date")
    min_weight = st.number_input("Minimum Weight (kg)", min_value=0.0)
    max_weight = st.number_input("Maximum Weight (kg)", min_value=0.0)
    healthy_lunch = st.checkbox("Healthy Lunch")
    healthy_dinner = st.checkbox("Healthy Dinner")
    no_other_snacks = st.checkbox("No other snacks")
    distance_800cal = st.number_input("800cal (Distance in km)", min_value=0.0)
    distance_200cal = st.number_input("200 cal (Distance in km)", min_value=0.0)
    badminton = st.checkbox("Badminton")
    if st.button("Submit"):
        st.write("Clicked Save")
        delta_backlog=0
        if healthy_lunch==False:
            delta_backlog+=12
        if healthy_dinner==False:
            delta_backlog+=12
        if no_other_snacks==False:
            delta_backlog+=12
        delta_backlog=delta_backlog-min(0,distance_800cal-12)-max(0,distance_800cal-12)
        if badminton==False:
            delta_backlog=delta_backlog-min(0,distance_200cal-4)-max(0,distance_200cal-4)
        elif badminton==True:
            delta_backlog=delta_backlog-distance_200cal
        backlog = backlog + delta_backlog
        write_backlog(backlog)
        new_record = {
            "Date": date,
            "Minimum Weight (kg)": min_weight,
            "Maximum Weight (kg)": max_weight,
            "Healthy Lunch (True/False)": healthy_lunch,
            "Healthy Dinner (True/False)": healthy_dinner,
            "No other snacks (True/False)": no_other_snacks,
            "800cal (Distance in km)": distance_800cal,
            "200 cal (Distance in km)": distance_200cal,
            "Badminton (True/False)": badminton
        }
        df.loc[len(df)] = new_record
        df.to_csv(csv_file, index=False)
        st.success("Record added successfully")
        st.rerun()
# def add_record():
#     with st.form("add_record_form"):
#         st.write("Add a new record")
#         date = st.date_input("Date")
#         min_weight = st.number_input("Minimum Weight (kg)", min_value=0.0)
#         max_weight = st.number_input("Maximum Weight (kg)", min_value=0.0)
#         healthy_lunch = st.checkbox("Healthy Lunch")
#         healthy_dinner = st.checkbox("Healthy Dinner")
#         no_other_snacks = st.checkbox("No other snacks")
#         distance_800cal = st.number_input("800cal (Distance in km)", min_value=0.0)
#         distance_200cal = st.number_input("200 cal (Distance in km)", min_value=0.0)
#         badminton = st.checkbox("Badminton")
        
#         save_button = st.form_submit_button("Save")
#         cancel_button = st.form_submit_button("Cancel")
        
#         if save_button:
#             st.write("Clicked Save")
#             new_record = {
#                 "Date": date,
#                 "Minimum Weight (kg)": min_weight,
#                 "Maximum Weight (kg)": max_weight,
#                 "Healthy Lunch (True/False)": healthy_lunch,
#                 "Healthy Dinner (True/False)": healthy_dinner,
#                 "No other snacks (True/False)": no_other_snacks,
#                 "800cal (Distance in km)": distance_800cal,
#                 "200 cal (Distance in km)": distance_200cal,
#                 "Badminton (True/False)": badminton
#             }
#             df.loc[len(df)] = new_record
#             df.to_csv(csv_file, index=False)
#             st.success("Record added successfully")
#             st.experimental_rerun()

# Display the table
st.title('Weight Tracker')
st.write(f'Backlog: {backlog}')
st.write('Here is the table from the CSV file:')
st.table(df)

# Add Record button
if st.button("Add Record"):
    add_record()

# Plot the weight trends
st.write('Weight Trends')
fig, ax = plt.subplots()
ax.plot(pd.to_datetime(df['Date']), df['Minimum Weight (kg)'], label='Min Weight (kg)')
ax.plot(pd.to_datetime(df['Date']), df['Maximum Weight (kg)'], label='Max Weight (kg)')

# Calculate Minimum Ideal Weight and Maximum Ideal Weight trends
start_date = pd.to_datetime('2025-03-03')
end_date = pd.to_datetime(df['Date'].max())
date_range = pd.date_range(start=start_date, end=end_date)

min_ideal_weight_start = 103.5
max_ideal_weight_start = 104.85
min_ideal_weight_trend = [min_ideal_weight_start - 0.15 * (date - start_date).days for date in date_range]
max_ideal_weight_trend = [max_ideal_weight_start - 0.15 * (date - start_date).days for date in date_range]

ax.plot(date_range, min_ideal_weight_trend, label='Min Ideal Weight (kg)', linestyle='--')
ax.plot(date_range, max_ideal_weight_trend, label='Max Ideal Weight (kg)', linestyle='--')

ax.set_xlabel('Date')
ax.set_ylabel('Weight (kg)')
ax.legend()
st.pyplot(fig)

# Calculate height in meters (6 feet 3 inches)
height_m = (6 * 0.3048) + (3 * 0.0254)

# Calculate BMI
df['Min BMI'] = df['Minimum Weight (kg)'] / (height_m ** 2)
df['Max BMI'] = df['Maximum Weight (kg)'] / (height_m ** 2)

# Plot the BMI trends
st.write('BMI Trends')
fig, ax = plt.subplots()
ax.plot(pd.to_datetime(df['Date']), df['Min BMI'], label='Min BMI')
ax.plot(pd.to_datetime(df['Date']), df['Max BMI'], label='Max BMI')
ax.set_xlabel('Date')
ax.set_ylabel('BMI')
ax.legend()
st.pyplot(fig)

# Display BMI ranges
st.write('BMI Ranges:')
st.write('Underweight: BMI < 18.5')
st.write('Normal weight: 18.5 <= BMI < 24.9')
st.write('Overweight: 25 <= BMI < 29.9')
st.write('Obesity: BMI >= 30')

st.write('Ideal Weight Range:')
min_ideal_weight = 18.5 * (height_m ** 2)   # BMI = 18.5
max_ideal_weight = 24.9 * (height_m ** 2)   # BMI = 24.9
st.write(f'Min Ideal Weight: {min_ideal_weight:.2f} kg')
st.write(f'Max Ideal Weight: {max_ideal_weight:.2f} kg')