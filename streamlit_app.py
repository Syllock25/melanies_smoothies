# CUSTOM SMOOTHIE ORDER FORM

# Import python packages
import streamlit as st
import requests                  # Pythan package to request simple API calls

# Snowpark is a library of 'packages' of functions python/../..
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

# Name box widget
name_on_order = st.text_input("Name on smoothie")
st.write("The name of your smoothie will be: ", name_on_order)

# Specific change for Streamlit not in Snowflake SniS
# Establish connection to Snowpart session (!)
cnx = st.connection("mrs_session")
session = cnx.session()

# Confirm that connection to Snowflake functions
# cur_user = cnx.query("SELECT current_account() as curacc, current_session() as curses, current_database() as curdb, current_warehouse() as curwh, current_user() as curusr, current_role() as currole, current_schema() as curschema;")
#st.write(cur_user)

# Change display of table to a multi-line selection => selection of fruits
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections=5            # We want 5 fruits, but maybe the system counts 0, 1, 2 ...
)

# Following syntax means that if ingredients_list is not null, then...
if ingredients_list:
    st.write(ingredients_list)
    # st.text(ingredients_list)
    
# Convert the list from multiselect to a string, we can store for orders
    ingredients_string = ''    # This ensures that python will perceive the variable as a string

# for loop construction to list items to string, the block is marked the indention
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '   # Note the increment operator, we append 'each_fruit' to 'ingredients_string'
        st.subheader(each_fruit + ' Nutrition Informatin')
        # Old / legacy API in course material, but seemingly the one that works
        fruit_nutrition = requests.get(f"https://fruityvice.com/api/fruit/{each_fruit}")
        fruit_data = fruit_nutrition.json()                                                   # Extract the data from the json format
        fruity_df = st.dataframe(data=fruit_data, use_container_width=True)                   # Make a Streamlit object - data frame

# Prepare insertion of orders in table, version two with order name
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order + """')"""

# Insert the Order into Snowflake with a Submit action
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")
