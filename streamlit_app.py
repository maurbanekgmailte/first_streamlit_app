import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🍞🥑Avocado toast')   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
# create the repeatable code block (called function)
def get_fruityvice_data(this_fruit_choise):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choise)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return(fruityvice_normalized)
# New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)    
except URLError as e:
  streamlit.error()

# organize the code for snowflake
streamlit.header("The Fruit load list contains:")
# snowflake related function
def get_fruit_load_list():  
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
# add a button to load the fruit
if stramlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# don't run anything past here while we troubleshoot
streamlit.stop()
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
streamlit.write('Thank you for adding ', add_my_fruit)
