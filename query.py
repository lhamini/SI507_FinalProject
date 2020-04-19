import plotly.graph_objs as go
import secrets
import sqlite3

app = Flask(__name__)

DBNAME = 'PlaneCrashes.sqlite'
mapbox_access_token = secrets.mapbox_token

def db_connection_setup(query):
    ''' Constructs database connection

    Parameters
    ----------
    query: string
        SQL query

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

def agg_for_each_year(year):
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    query=f'''
    SELECT strftime("%Y", date) as year, count(*), sum(fatalities)
    FROM Crashes
    GROUP BY year
    HAVING year = "{year}"
    '''
    return db_connection_setup(query)

def question1():
    query='''
        SELECT name, region, alpha2Code, latlng, flag, count(*), sum(fatalities) FROM Crashes
    	JOIN Countries
    	On Crashes.countryId = Countries.Id
        GROUP By name
        ORDER BY count(*) DESC
    '''
    return db_connection_setup(query)

def crash_year_list():
    query='''
        SELECT DISTINCT strftime("%Y", date) as year
        From Crashes
    '''
    return db_connection_setup(query)

def crashes_for_each_year(year, sort):
    if sort == "country":
        sort='name'
    query=f'''
        SELECT strftime("%Y", date) as year, date, name, fatalities, occupants
        FROM Crashes
        JOIN Countries
        ON Crashes.countryId = Countries.Id
        WHERE year=="{year}"
        ORDER BY {sort} DESC
    '''
    return db_connection_setup(query)

def map_query(year, sort):
    if sort == "country":
        sort='name'
    query=f'''
        SELECT strftime("%Y", date) as year, name, region, alpha2Code, latlng, flag, count(*), sum(fatalities)
	    FROM Crashes
        JOIN Countries
        ON Crashes.countryId = Countries.Id
        WHERE year=="{year}"
        GROUP BY name
        ORDER BY {sort} DESC
    '''
    return db_connection_setup(query)

def plot_map(year, sort):
    results = map_query(year, sort)
    crash_lat = []
    crash_lon = []
    crash_country_name = []
    for r in results:
        latpos = r[4].find(',')
        lat = r[4][1:latpos]
        lon = r[4][latpos+1:-1]
        crash_lat.append(lat)
        crash_lon.append(lon)
        crash_country_name.append(r[1])

    data_map = go.Figure(go.Scattermapbox(
            lat = crash_lat,
            lon= crash_lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=15,
                color='Red'
            ),
            text = crash_country_name
        ))

    data_map.update_layout(
            title="Map of all crashes in this year",
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style="outdoors",
                bearing=0,
                pitch=0,
                zoom=1.2
            ),
        )

    fig = go.Figure(data=data_map)
    div = fig.to_html(full_html=False)
    return div

def plot_bar(year, sort):
    results = crashes_for_each_year(year, sort)
    x_axis = list(range(len(results)))
    y_axis = [r[3] for r in results]
    y_axis2 = [r[4] for r in results]


    data_bar = go.Figure()
    data_bar.add_trace(go.Bar(

            x=x_axis,
            y=y_axis2,
            name='All occupants',
            marker_color='indianred'

    ))

    data_bar.add_trace(go.Bar(
        x=x_axis,
        y=y_axis,
        name='Fatalities',
        marker_color='lightsalmon'
    ))

    data_bar.update_layout(autosize=True,
                           barmode='group',
                           title="Comparison of the number of death/occupants in each crash",
                           xaxis_title="Crashes",
                           yaxis_title="Number of all accupants/fatalities")

    fig = go.Figure(data=data_bar)
    div = fig.to_html(full_html=False)
    return div


def crash_details_query(date):
    query=f'''
    SELECT  name, date, location, departure, destination, operator, occupants, fatalities, summary
    FROM Crashes
    JOIN Countries
    ON Crashes.countryId = Countries.Id
    WHERE date = "{date}"
    '''
    return db_connection_setup(query)
