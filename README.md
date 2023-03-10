# sqlalchemy-challenge

## Description
This is a two part project. The first part involves using SQLAlchemy to create an ORM in order to query a SQLite database of climate data and peform some analysis on the resulting data. The second part involves using flask to host an API website that allows users to query the database.

## Part 1: Exploring and analysing climate data

#### Setup

- Use SQLAlchemy create_engine() function to connect to the SQLite database.
- Use the SQLAlchemy automap_base() function to reflect the tables into classes, and then save references to the classes.
- Link Python to the database by creating a SQLAlchemy session.

From this we find that we have two tables, a station table which contains the ID and names of 9 weather stations in Hawaii, and a measurements table which contains precipitation and temperature data collected at these 9 stations between 01-01-2010 and 23-08-2017.

#### Analysis
 
 - Precipitation analysis
 
 This involved querying the most recent 12 months of the dataset for precipitation values along with the dates, loading the data into a Pandas DataFrame, sorting the data frame values by date and plotting and saving an image of a graph showing date vs inches of rainfall. The following is the graph produced:
 
![precipitaton](https://user-images.githubusercontent.com/119974799/224215042-052bf182-6d94-45ff-929f-3d99bd8b6e50.png)

Also summary statistics were collected for the data:

![Screenshot 2023-03-09 221649](https://user-images.githubusercontent.com/119974799/224214515-f96b4d70-3821-4a7d-a0ce-0d80116983d7.png)


- Station/Temperature analysis

This involved querying the data to find the number of weather stations, the most active station, the lowest, highest and average temperatures recorded for the most active station and finally collecting the most recent 12 months of temperature data for the most active station, plotting a histogram of the temperature data as a histogram and saving the image. The following graph was produced:

![temperature](https://user-images.githubusercontent.com/119974799/224218189-ffe38a74-40fc-4371-a318-843bdd79e977.png)

## Part 2: Climate App

#### Setup

Created a Flask API based on the queries developed in part 1 to return data to users in JSON format. Below are the end points.

#### Endpoints

- /

This is the homepage which lists the available endpoints

- /api/v1.0/precipitation

Retrieves the most recent 12 months of precipitation data for the weather stations by date

- /api/v1.0/stations

Retrieves a list of all stations in the dataset

- /api/v1.0/tobs

Retrieves temperature measurements along with dates for the most recent 12 months for the most active weather station

- /api/v1.0/<start>
 
Takes a starting date and retrieves the minimum, average and maximum temperatures in the data set from the starting date to the most recent measurement date. Date must be entered in YYYY-MM-DD format
