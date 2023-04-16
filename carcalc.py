import pandas as pd
import numpy_financial as npf
import plotly.express as px
import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header



# Read the existing data from a CSV file
df = pd.read_csv("car_payment_calc2.csv")
rain(
    emoji="🎈",
    font_size=24,
    falling_speed=8,
    animation_length="infinite",
)

colored_header(
    label="Car Loan Caculator Details",
    description="The Car Loan Calculator allows you to update car loan details and calculates the monthly payment, total interest paid, and total loan cost. It validates input and saves updated data as a CSV file. Simply enter loan amount, interest rate, loan term, down payment, and taxes, then click Add Data to see results.",
    color_name="green-70",
)

# Function to calculate monthly interest paid
def calculate_interest_paid(loan_amount, interest_rate, loan_term_months, down_payment, taxes_fees):
    present_value = loan_amount - down_payment + taxes_fees
    monthly_rate = interest_rate / 12
    monthly_term = loan_term_months
    monthly_payment = -npf.pmt(monthly_rate, monthly_term, present_value)
    total_interest_paid = (monthly_payment * monthly_term) - present_value
    return total_interest_paid

# Display the existing data in the app
save_data = st.button('Save File')
st.header('Enter Car Loan Details')
st.write(df)

# Sidebar for user input
st.sidebar.header("Calculator")
options_form = st.sidebar.form("Update Calculations")

# User input fields with validation
loan_amount_label = options_form.text_input("Loan Amount (USD)", key='loan_amount')
interest_rate_label = options_form.text_input("Interest Rate (%)", key='interest_rate')
loan_term_label = options_form.text_input("Loan Term (Months)", key='loan_term')
down_payment_label = options_form.text_input("Down Payment Amount (USD)", key='down_payment')
taxes_fees_label = options_form.text_input("Taxes Amount (USD)", key='taxes_fees')
add_data = options_form.form_submit_button("Press for Output")

if add_data:
    # Perform input validation
    if not loan_amount_label or not interest_rate_label or not loan_term_label:
        st.warning("Please enter valid values for Loan Amount, Interest Rate, and Loan Term.")
    else:
        try:
            # Convert user input to numeric values
            loan_amount = float(loan_amount_label)
            interest_rate = float(interest_rate_label) / 12
            loan_term_months = int(loan_term_label)
            down_payment = float(down_payment_label) if down_payment_label else 0
            taxes_fees = float(taxes_fees_label) if taxes_fees_label else 0

            # Perform additional validation
            if loan_amount <= 0 or interest_rate <= 0 or loan_term_months <= 0:
                st.warning("Loan Amount, Interest Rate, and Loan Term must be positive values.")
            else:
                # Calculate monthly payment using numpy_financial
                present_value = loan_amount - down_payment + taxes_fees
                monthly_rate = interest_rate / 100
                monthly_term = loan_term_months
                monthly_payment = -npf.pmt(monthly_rate, monthly_term, present_value)

                # Calculate total interest paid
                total_interest_paid = calculate_interest_paid(loan_amount, interest_rate, loan_term_months, down_payment, taxes_fees)
                 # Calculate total loan cost
                total_loan_cost = loan_amount + total_interest_paid

                # Create a new row with user input and calculated values
                new_row = pd.DataFrame({'Loan Amount (USD)': [loan_amount],
                                        'Interest Rate (%)': [interest_rate_label],
                                        'Loan Term (Months)': [loan_term_months],
                                        'Down Payment Amount (USD)': [down_payment_label],
                                        'Taxes Amount (USD)': [taxes_fees_label],
                                        'Monthly Payment (USD)': [monthly_payment],
                                        'Total Interest Paid (USD)': [total_interest_paid],
                                        'Total Loan Cost': [total_loan_cost]})

                # Append the new row to the DataFrame
                df = df.append(new_row, ignore_index=True)

                # Display the updated DataFrame
                st.write(df)
                st.success("Data added successfully.")
        except ValueError:
            st.warning("Please enter valid numeric values for Loan Amount, Interest Rate, and Loan Term.")

# Save data to CSV file
if save_data:
    df.to_csv("car_payment_calc2.csv", index=False)
    st.success("Data saved to CSV file.")

