# Cargo Vessel Analysis

# Project Summary

### File Structure

- `assignment/`  

- `sql/` 

  - `queries.sql`

- `__ main__ .py`

- `requirements.txt`

- `code/`
-   `main.py`
  
  -    `bounding_box_analysis.ipynb`
  
  -   `temporal_analysis.ipynb`

- `data/` 

  - `CSV files`

- `data_cleanup/`
-   `truncate_csv.py`

- `instructions/`
-     `Assignment.docx`
-     `DataDictionary.pdf` 

### Steps

- Set up a Postgresql database and insert the coordinate data and ais data in it (sql/queries.sql).
- Find the dimensions for the bounding box using nearest neighbors and density estimation (code/bounding_box_analysis.ipynb)
- The NAIS website specifies the cargo vessel_type as any number between 70 and 79, inclusive. All AIS data is filtered to only contain these vessel_type codes.
- Write a function to take in the port code and output the unique number of cargo vessels by day (code/main.py).
- Analyse the traffic of vessels within the bounding box by hour of the day, across two days (code/temporal_analysis.ipynb).

# Installation Guide

- Create a directory to pull the code to:
`mkdir assignment`
- Change directory (assuming it’s called assignment):
`cd assignment`
- Initialize an empty repository:
`git init`
- Clone the following repository by running the following command: 
`git clone https://github.com/ananditabodas/DPWorldAssignment.git`
- Create a .env file in the root directory and enter the following details:

```python
DB_NAME="dbname"
DB_USER="dbuser"
DB_PASSWORD="dbpassword"
DB_HOST="ipaddress"
DB_PORT= 5432
```

- Install all the packages required:
`pip install -r requirements.txt`
- Run the code to get a date-wise number of cargo vessels (remove the spaces between the underscores): 
`python3 __ main__. py`

<aside>
💡 Note: This repository doesn’t contain any of the original CSV files. It assumes that a database set up is already present. If not, the queries within `sql/queries.sql` can be run using the `psql` command in Linux.

</aside>

# Observations

The assumption is that there will be a larger concentration of vessels near the port. So the confines of the bounding box are defined with the help of a hexbin density plot. It results in a bounding box of dimensions:

- width in degrees- 0.035866
- height in degrees- 0.041723

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/15723fa7-0d43-4f55-80c8-d4de4b144322/971f39a0-c4fe-4fbd-ad19-4b52108881d6/Untitled.png)

Since vessels remain relatively stationary through the day, an hourly study of traffic seems like the appropriate resolution.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/15723fa7-0d43-4f55-80c8-d4de4b144322/3a6e2ef2-bdb8-4201-bc63-0fa88d3d331a/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/15723fa7-0d43-4f55-80c8-d4de4b144322/bb1529d1-4b7f-49a8-ad89-77ec845439ec/Untitled.png)

The total cargo vessels on 1st January, 2020 were 10 and on 2nd January, 2020 were 17.

Although there is a 70% rise in the traffic from the 1st of January, 2020 to the 2nd of January, 2020, it is a rise of 7 in absolute terms. Whether this is a spike or not cannot be determined without additional data about the average vessels received per day.

If we assume that there is a spike in the incoming vessels, these could be the reasons:

- 1st of January is a public holiday and could be a reason for fewer vessels entering the port.
- There may have been delays on the 1st of January due to poor weather conditions causing vessels to arrive on 2nd January instead.
