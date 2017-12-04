
import urllib.request, json
import pandas as pd
import MySQLdb as mdb

con = mdb.connect(host = 'localhost',
                  user = 'root',
                  passwd = 'dwdstudent2015',
                  charset='utf8', use_unicode=True);

# Run a query to create a database that will hold the data
db_name = 'final_project'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)

# Create a database
cursor = con.cursor()
cursor.execute(create_db_query)
cursor.close()

cursor = con.cursor()
table_name = 'event_bot'
create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table}
                                (title VARCHAR(100),
                                url VARCHAR(1000),
                                start_time VARCHAR(100),
                                category VARCHAR(100),
                                min_price VARCHAR(100),
                                max_price VARCHAR(100),
                                zip_code VARCHAR(100),
                                venue VARCHAR(100),
                                lon VARCHAR(100),
                                lat VARCHAR(100),
                                PRIMARY KEY(title)
                                )'''.format(db=db_name, table=table_name)
cursor.execute(create_table_query)
cursor.close()
 In[199]:


def extract_columns(json):
    title = json['_embedded']['events'][0]['name']
    url = str(json['_embedded']['events'][0]['url'])
    start_time = json['_embedded']['events'][0]['dates']['start']['dateTime']
    category = json['_embedded']['events'][0]['classifications'][0]['segment']['name']
    min_price = str(json['_embedded']['events'][0]['priceRanges'][0]['min'])
    max_price = str(json['_embedded']['events'][0]['priceRanges'][0]['max'])
    zip_code = json['_embedded']['events'][0]['_embedded']['venues'][0]['postalCode']
    venue = json['_embedded']['events'][0]['_embedded']['venues'][0]['name']
    lon = json['_embedded']['events'][0]['_embedded']['venues'][0]['location']['longitude']
    lat = json['_embedded']['events'][0]['_embedded']['venues'][0]['location']['latitude']


    extracted_json = {
        'title': title,
        'url': str(url),
        'start_time': start_time,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'zip_code': zip_code,
        'venue': venue,
        'lon': lon,
        'lat': lat
    }

    return extracted_json


def store_data(json):
    query_template = '''INSERT INTO {db}.{table}(title,
                                            url,
                                            start_time,
                                            category,
                                            min_price,
                                            max_price,
                                            zip_code,
                                            venue,
                                            lon,
                                            lat)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(db=db_name, table=table_name)
    cursor = con.cursor()

    title = json['title']
    url = json["url"]
    start_time = json['start_time']
    category = json["category"]
    min_price = json["min_price"]
    max_price = json["max_price"]
    zip_code = json['zip_code']
    venue = json['venue']
    lon = json['lon']
    lat = json['lat']
    query_parameters = (title, url, start_time, category, min_price, max_price, zip_code, venue, lon, lat)
    cursor.execute(query_template, query_parameters)

    con.commit()
    cursor.close()


def find_table(**kwargs):
    f = ['%s=%s' % (k, kwargs[k]) for k in dict(kwargs).keys()]
    query = '''SELECT * FROM `final_project`.`event_bot` WHERE %s'''.format(' AND '.join(f))
    cursor = con.cursor()
    cursor.execute(query)
    cursor.commit()
    data = cursor.fetch()
    cursor.close()
    return data


if __name__ == '__main__':
    with urllib.request.urlopen("https://app.ticketmaster.com/discovery/v2/events.json?size=1&apikey=80Yiy3BkF0kupWGVzo75UtuPdt1Vu1V3&startDateTime=2017-12-09T00:12:00Z") as url:
        json = json.loads(url.read().decode())

    dataframe = extract_columns(json)
    dataframe
