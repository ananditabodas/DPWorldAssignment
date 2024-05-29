'''
Code to only retain columns that will be inserted into the database.
This is done to make the import process possible from pgAdmin.
'''

import pandas as pd # type: ignore

# Read the original csv
updated_pub = pd.read_csv('../data/updatedPub150.csv')

columns_to_keep = [
    'World Port Index Number', 
    'Region Name', 
    'Main Port Name', 
    'UN/LOCODE', 
    'Country Code', 
    'Latitude', 
    'Longitude'
]

coordinate_data = updated_pub[columns_to_keep]

# Rename columns to match the column names in the database
coordinate_data.columns = [
    'world_port_index_number', 
    'region_name', 
    'main_port_name', 
    'un_locode', 
    'country_code', 
    'latitude', 
    'longitude'
]

# Save the new CSV
coordinate_data.to_csv('../data/coordinate_data.csv', index=False)
print ("Completed")