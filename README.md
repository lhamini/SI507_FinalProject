# World of Airplane Crashes 

You can find all informatin about major airplane crashes that has happend so far. (This project is the final project for the course SI-507 Python Programming)

## Description
You can explore airplane crashes in each year, find out where and why they happend, and many more information.

To start, you can choose a year, decide the sorting order (Fatalities/Date/Country), and the representatin you want to see (table/map). 

After submiting the request, you will see a new page showing the following results:

- Total number of major crashes in that year.
- Total number of deaths in those crashes.
- An interactive world map, showing crashes in that year.
- A bar chart comparing occupants/fatalities in that year.
- A table containing all crashes in that year. You can click on each date to find out more informatin about each specific crash.

After clicking on a date, you will see a new page showing the following results:

- Summary of what happend 
- Date
- Country
- Approximation location
- Departure
- Destination
- Operator
- Total number of ocuupants
- Total number of fatalities



### Install Requirements

- Flask 
- Plotly
- [Mapbox](https://www.mapbox.com) API key 

### Guide
plane_crash.py: scraping and saving data in csv format
database.py: create and populate database
app.py: establish the web interface


## Authors

* **Elham Amini** Data Science student at the University of Michigan School of Information

## Data Source 
[planecrash.info](http://www.planecrashinfo.com)


## Acknowledgments

* Mark Newman, awesome SI507 instroctor and his teaching team

