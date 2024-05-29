--Database name: postgres

--Create a user role and assign all permissions. This will be the admin.
CREATE ROLE postgres WITH LOGIN PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;

-- Create AIS data table
CREATE TABLE ais_data (
    ais_id serial PRIMARY KEY,
    mmsi text,
    base_date_time TIMESTAMP,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    sog FLOAT,
    cog FLOAT,
    heading FLOAT,
    vessel_name text,
    imo text,
    call_sign text,
    vessel_type INTEGER,
    status INTEGER,
    len FLOAT,
    width FLOAT,
    draft FLOAT,
    cargo text,
    transceiver_class text
);

-- Create port coordinates table
CREATE TABLE port_coordinates (
	coordinate_id SERIAL PRIMARY KEY,
    world_port_index_number FLOAT,
    region_name TEXT,
    main_port_name TEXT,
    un_locode TEXT,
    country_code TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

--Copy AIS data into AIS table
\copy ais_data(mmsi, base_date_time, lat, lon, sog, cog, heading, vessel_name, imo, call_sign, vessel_type, status, len, width, draft, cargo, transceiver_class) from '/home/ananditabodas/AIS_2020_01_01.csv
' with delimiter ',' csv header;

\copy ais_data(mmsi, base_date_time, lat, lon, sog, cog, heading, vessel_name, imo, call_sign, vessel_type, status, len, width, draft, cargo, transceiver_class) from '/home/ananditabodas/AIS_2020_01_02.csv
' with delimiter ',' csv header;

--Copy UpdatedPub150.csv into port_coordinates table 
--Since there are several columns that aren't required in the CSV, we will run data_cleanup/truncate_csv.py
--This will generate a new file called coordinate_data.csv
--We will be copying this file.
\copy port_coordinates(world_port_index_number, region_name, main_port_name, un_locode, country_code, latitude, longitude) from '/home/ananditabodas/coordinate_data.csv' with delimiter ',' csv header;
