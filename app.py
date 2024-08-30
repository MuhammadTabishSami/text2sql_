from dotenv import load_dotenv
load_dotenv() # load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model 
# and provide SQL query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    print('Response Object',response)

    # Assuming the response object has an attribute `text` or similar
    generated_sql = response.text if hasattr(response, 'text') else response[0].text

    # Remove any backticks and other Markdown formatting
    cleaned_sql = generated_sql.strip().strip('```sql').strip('```')
    return cleaned_sql


# Function to retrieve query from SQL database
def read_sql_query(sql,db):
    try:
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.OperationalError as e:
        print(f'OperationalError: {e}')
        return[]
    except Exception as e:
        print(f'An Error Occurred: {e}')
        return[]
    

# Defining Prompt to make Model understand our requirements
prompt = [
    """
    You are an expert in converting English questions to SQL queries!

    The SQL database has six tables as follows:

    Apartment_Bookings: (apt_booking_id, apt_id, guest_id, booking_status_code, booking_start_date, booking_end_date)
    Apartment_Buildings: (building_id, building_short_name, building_full_name, building_description, building_address, building_manager, building_phone)
    Apartment_Facilities: (apt_id, facility_code)
    Apartments: (apt_id, building_id, apt_type_code, apt_number, bathroom_count, bedroom_count, room_count)
    Guests: (guest_id, gender_code, guest_first_name, guest_last_name, date_of_birth)
    View_Unit_Status: (apt_id, apt_booking_id, statust_date, available_yn)
    When converting English questions to SQL queries, consider the following examples:

    Example 1: Simple Select Query

    Question: "Show me all the details of apartments."
    SQL: SELECT * FROM Apartments;
    Example 2: Conditional Select Query

    Question: "List the names of all buildings managed by 'John Doe'."
    SQL: SELECT building_full_name FROM Apartment_Buildings WHERE building_manager = 'John Doe';
    Example 3: Join Query

    Question: "Find the booking details for the apartment with apartment ID 'A101'."
    SQL: SELECT * FROM Apartment_Bookings WHERE apt_id = 'A101';
    Example 4: Aggregation Query

    Question: "How many apartments are in each building?"
    SQL: SELECT building_id, COUNT(*) as apartment_count FROM Apartments GROUP BY building_id;
    Example 5: Complex Join Query

    Question: "List the guest names and their booking statuses for all bookings starting after '2024-07-01'."
    SQL: SELECT g.guest_first_name, g.guest_last_name, ab.booking_status_code FROM Guests g JOIN Apartment_Bookings ab ON g.guest_id = ab.guest_id WHERE ab.booking_start_date > '2024-07-01';
    Example 6: Filtering with Multiple Conditions

    Question: "Show the available units as of '2024-07-15'."
    SQL: SELECT * FROM View_Unit_Status WHERE statust_date = '2024-07-15' AND available_yn = 'Y';
    When converting English questions to SQL:

    Ensure that table and column names are used correctly.
    Join tables where necessary to retrieve information across multiple tables.
    Apply appropriate filtering conditions (WHERE clauses) based on the query requirements.
    Aggregate data when needed (e.g., using COUNT, SUM, AVG, etc.).
    Order the results if specified (e.g., using ORDER BY).

    """
]

# Creating streamlit app
st.set_page_config(page_title='I can retrieve any SQL Query')
st.header('Text2SQL Generator using LLM')

question=st.text_input('Input: ',key='input')

submit=st.button('Ask the Question')

# if submit button gets clicked
if submit:
    response=get_gemini_response(question,prompt)
    print('Generated SQL Query:',response)
    db_path = r'F:\DS\text2sql\apartment_rentals.sqlite' 
    data=read_sql_query(response, db_path)
    st.subheader('The Response is:')
    for row in data:
        print(row)
        st.header(row)
       
