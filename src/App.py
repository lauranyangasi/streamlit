# Import necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import time
import pickle

# Define app sections
header = st.container()
dataset = st.container
prediction = st.container



# Insert headers and image
st.header("Welcome to Sales Prediction")
st.subheader("To help you know your future sales 📈...")
st.image("src/images/san_diego.jpeg")

#preview the provided data set data set
with header:
    preview = st.button ("Preview the Dataset")
    if preview:
        data = pd.read_csv(r"prediction_results.csv")
        st.dataframe = data
        st.write("These are the first 10 rows of the dataset")
        st.write(data.head(10))
        st.write(data.describe())

form = st.form(key = "Information", clear_on_submit = True)

# Define expected inputs from the user
input_col = ["frequency", "Store_nbr", "Onpromotion", "Family", "City",

]
Disp_results = pd.DataFrame()  # Initialize for download

# Create a function to convert the results DataFrame to CSV
def convert_to_csv(df):
    return df.to_csv()
   
# Taking input from the user
with st.form("This form", clear_on_submit=True):
    st.subheader("Enter the number of day(s)/week(s) you want to predict, And the frequency as D for Daily or W for weekly")
    frequency = str(st.text_input("Frequency 'D' for Daily 'W' for weekly ")).upper()
    Number_of_days = int(st.number_input("Please enter number of day(s)/week(s)"))
    Store_nbr = int(st.number_input("Please enter the store number"))
    Onpromotion = int(st.number_input("Please enter number of items onpromotion"))
    Family = st.text_input("Please input the family of the store")
    City = st.text_input("Please enter the city")


    submit = st.form_submit_button("Predict your sales")

if submit:
    # Check if the inputs are valid
    if frequency not in ('D', 'W') or Number_of_days <= 0:
        st.error("Please enter a valid frequency ('D' or 'W') and a positive number of days.")
    else:
        # Success message
        st.success("Inputs received successfully ✅")

        try:
            # Generate dummy random data for demonstration purposes
            date_range = pd.date_range(start=pd.Timestamp.today(), periods=Number_of_days, freq=frequency)
            np.random.seed(0)
            random_sales = np.random.randint(50, 200, size=Number_of_days)
            random_lower = random_sales - np.random.randint(10, 30, size=Number_of_days)
            random_upper = random_sales + np.random.randint(10, 30, size=Number_of_days)

            # Create a DataFrame with the dummy data
            dummy_data = pd.DataFrame({
                'Date': date_range,
                'lowest Expected sales': random_lower,
                'Highest Expected Sales': random_upper,
                'Expected Sales': random_sales
            })

            # Display a success message with balloons animation
            with st.spinner("Prediction in progress..."):
                time.sleep(2)
                st.balloons()
                st.success("Great✅")

            # Display the predicted sales in a DataFrame
            if frequency == "W":
                output_frequency = 'Week(s)'
            else:
                output_frequency = 'Day(s)'
            
            st.write(f"These are your predicted sales in the next {Number_of_days} {output_frequency}")
            st.dataframe(dummy_data)

            # Display a line chart of predicted sales
            st.title(f"Line Graph Of Predicted Sales Over {Number_of_days} {output_frequency} ")
            st.line_chart(data=dummy_data.set_index('Date'), use_container_width=True)

            # Create an expander for downloading results as CSV
            expand = st.expander('Download Results as CSV')
            with expand:
                st.download_button(
                    'Download results',
                    convert_to_csv(dummy_data),
                    'prediction_results.csv',
                    'text/csv',
                    'download'
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
