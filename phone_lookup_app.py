
import pandas as pd
import streamlit as st

# Function to load the reference data (Area Codes Lookup)
@st.cache_data
def load_reference_data():
    area_codes_lookup = pd.read_excel('Area Codes Lookup.xlsx')  # Reference sheet
    return area_codes_lookup

# Function to process the phone numbers
def process_phone_numbers(file, area_codes_lookup):
    # Read the input Excel file
    phone_data = pd.read_excel(file)

    # Extract the first 3 digits (area code) from phone numbers
    phone_data['Area Code'] = phone_data['phone'].astype(str).str[:3]

    # Perform lookup using the area code
    result = pd.merge(phone_data, area_codes_lookup, left_on='Area Code', right_on='Prefix', how='left')

    # Select only the columns you need in the final output
    result_final = result[['phone', 'State', 'City', 'Zip', 'TimeZone']]
    
    return result_final

# Main app code
st.title("Phone Number to Geo Info Lookup App")

# File upload
uploaded_file = st.file_uploader("Upload Excel file with phone numbers", type=["xlsx"])

# If file is uploaded
if uploaded_file is not None:
    # Load the reference data
    area_codes_lookup = load_reference_data()

    # Process the uploaded phone numbers
    result = process_phone_numbers(uploaded_file, area_codes_lookup)

    # Display the result in the app
    st.write(result)

    # Provide an option to download the result as an Excel file
    result.to_excel("processed_phone_numbers.xlsx", index=False)
    st.download_button(label="Download the result as Excel",
                       data=open("processed_phone_numbers.xlsx", "rb").read(),
                       file_name="processed_phone_numbers.xlsx")
