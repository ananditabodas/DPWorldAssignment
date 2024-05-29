import psycopg2 
import pandas as pd 
import os 
from dotenv import load_dotenv

'''
Contains all the functions required to get the unique vessels per day.
'''

# Load environment variables from the .env file
load_dotenv()

'''
Note: create a .env in the root folder file with the following details:
DB_NAME="dbname"
DB_USER="dbuser"
DB_PASSWORD="dbpassword"
DB_HOST="ipaddress"
DB_PORT= 5432
'''

def connect_to_database():

    '''
    Get the database configuration from environment variables
    '''

    dbname_var = os.getenv('DB_NAME')
    user_var = os.getenv('DB_USER')
    password_var = os.getenv('DB_PASSWORD')
    host_var = os.getenv('DB_HOST')
    port_var=os.getenv('DB_PORT')

    conn= psycopg2.connect(dbname=dbname_var, user=user_var, password=password_var, host=host_var, port=port_var)  #
    cur= conn.cursor()

    return conn, cur

def close_database(conn, cur):
    conn.close()
    cur.close()

def get_latitude_longitude(cur, port_code='US LGB'):

    '''
    Get the port coordinates of a given port code. If left blank, the default port_code is US LGB
    '''

    get_lat_lon= """select latitude, longitude from port_coordinates where un_locode = %s;"""
    cur.execute(get_lat_lon, (port_code,))
    latitude, longitude = cur.fetchone()
    return latitude, longitude


def get_ships_in_vicinity(cur, latitude, longitude, width= 0.035866, height=0.041723 ):

    '''
    This function returns a dataframe of cargo vessels within the bounding box 
    with its datetime, latitude and longitude.
    Default width and height of bounding box is specified, but can be overwritten if required.
    '''

    #Additional Information:
    #-The NAIS website lists all vessel types between 70 and 79, inclusive, as cargo ships.
    #The bounding box dimensions have been derived in bounding_box_analysis.ipynb using the 
    #coordinates for Long Beach Port as centre.

    get_ships_in_vicinity= """select base_date_time, imo, vessel_name, lat, lon from ais_data 
    where (lat between %s and %s)
    and (lon between %s and %s) and 
    vessel_type>69 and vessel_type <80
    """
    cur.execute(get_ships_in_vicinity, (latitude-height, latitude+height, longitude- width, longitude+ width))
    ships_in_vicinity_df = pd.DataFrame(cur.fetchall(), columns=['datetime', 'imo', 'vessel_name', 'latitude', 'longitude'])
    return ships_in_vicinity_df

def get_unique_ships_per_day(ships_in_vicinity_df):

    '''
    Returns the unique count of cargo vessels in a 24 hour frame.

    '''

    ships_in_vicinity_df['date']= ships_in_vicinity_df['datetime'].dt.date
    unique_ships_per_day_df= ships_in_vicinity_df.groupby(['date'])['imo'].nunique().reset_index()
    unique_ships_per_day_df.columns= ['Date', 'Cargo Vessel Count']
    return unique_ships_per_day_df

def get_cargo_vessels(port='US LGB'):

    '''
    This is the parent calling function that runs all the components together.
    It takes in a port code as input and prints the number of cargo vessels in the day, 
    as well as returns the same data in a pandas dataframe
    '''

    conn, cur= connect_to_database()
    latitude, longitude= get_latitude_longitude(cur, port)
    ships_in_vicinity_df = get_ships_in_vicinity(cur, latitude, longitude, width= 0.035866, height=0.043723 )
    unique_ships_per_day_df = get_unique_ships_per_day(ships_in_vicinity_df)
    close_database(conn, cur)
    print (unique_ships_per_day_df)
    return unique_ships_per_day_df



