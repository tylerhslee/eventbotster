# -*- coding: utf-8 -*-
'''
Connect to the database
'''
import urllib.request, json
import pandas as pd
import MySQLdb as mdb
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

con = mdb.connect(host = '54.198.181.165',
                  user = 'finalpadmin',
                  passwd = 'IWroteAGoodCFE',
                  charset='utf8', use_unicode=True);

# Run a query to create a database that will hold the data
db_name = 'final_project'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)

# Create a database
cursor = con.cursor()
cursor.execute(create_db_query)

table_name = 'event_bot'
create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table}
                                (title VARCHAR(100),
                                url VARCHAR(1000) NOT NULL,
                                start_time VARCHAR(100),
                                std_time VARCHAR(100),
                                category VARCHAR(100),
                                min_price VARCHAR(100),
                                max_price VARCHAR(100),
                                zip_code VARCHAR(100),
                                venue VARCHAR(100),
                                lon VARCHAR(100),
                                lat VARCHAR(100),
                                PRIMARY KEY(url)
                                )'''.format(db=db_name, table=table_name)
cursor.execute(create_table_query)
cursor.close()


def extract_data(row, *args):
    t = row
    for key in args:
        try:
            t = t[key]
        except KeyError:
            return 'NA'
    return t


def get_titles():
    cursor = con.cursor()
    title_query = '''SELECT title FROM final_project.event_bot'''
    cursor.execute(title_query)
    con.commit()
    data = cursor.fetchall()
    titles = set([title.lower() for tup in data for title in tup])
    cursor.close()
    return ','.join(titles)


def extract_columns(json):
    data = json['_embedded']['events']

    title = [extract_data(k, 'name') for k in data]
    url = [k['url'] for k in data]
    start_time = [extract_data(k, 'dates', 'start', 'dateTime') for k in data]
    category = [k['classifications'][0]['segment']['name'] for k in data]
    min_price = [extract_data(k, 'priceRanges', 0, 'min') for k in data]
    max_price = [extract_data(k, 'priceRanges', 0, 'max') for k in data]
    zip_code = [k['_embedded']['venues'][0]['postalCode'] for k in data]
    venue = [k['_embedded']['venues'][0]['name'] for k in data]
    lon = [k['_embedded']['venues'][0]['location']['longitude'] for k in data]
    lat = [k['_embedded']['venues'][0]['location']['latitude'] for k in data]
    
    extracted_json = []
    
    for i in range(len(title)):
        extracted_json.append({
            'title': title[i],
            'url': str(url[i]),
            'start_time': start_time[i],
            'category': category[i],
            'min_price': min_price[i],
            'max_price': max_price[i],
            'zip_code': zip_code[i],
            'venue': venue[i],
            'lon': lon[i],
            'lat': lat[i]
        })
    pp.pprint(extracted_json[0])
    
    return extracted_json


def store_data(data):
    num_rows = len(data)
    values = ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'] * num_rows)
    query_template = '''INSERT IGNORE INTO {db}.{table}(title,
                                            url,
                                            start_time,
                                            std_time,
                                            category,
                                            min_price,
                                            max_price,
                                            zip_code,
                                            venue,
                                            lon,
                                            lat)
                    VALUES {values}'''.format(db=db_name, table=table_name, values=values)
    cursor = con.cursor()

    title = [json['title'] for json in data]
    url = [json['url'] for json in data]
    start_time = [json['start_time'] for json in data]
    std_time = [json['std_time'] for json in data]
    category = [json['category'] for json in data]
    min_price = [json['min_price'] for json in data]
    max_price = [json['max_price'] for json in data]
    zip_code = [json['zip_code'] for json in data]
    venue = [json['venue'] for json in data]
    lon = [json['lon'] for json in data]
    lat = [json['lat'] for json in data]
    combined = list(zip(title, url, start_time, std_time, category, min_price, max_price, zip_code, venue, lon, lat))
    query_parameters = tuple([j for i in combined for j in i])
    cursor.execute(query_template, query_parameters)

    con.commit()
    cursor.close()


def find_data(**kwargs):
    f = ["%s='%s'" % (k, kwargs[k]) for k in dict(kwargs).keys()]
    print(f)
    query = '''SELECT * FROM `final_project`.`event_bot` WHERE {q}'''.format(q=' AND '.join(f))
    cursor = con.cursor()
    cursor.execute(query)

    con.commit()
    data = cursor.fetchall()
    ret = []
    for (title, url, start_time, std_time, category, min_price, max_price, zip_code, venue, lon, lat) in data:
        ret.append({
            'title': title,
            'url': url,
            'start_time': start_time,
            'std_time': std_time,
            'category': category,
            'min_price': min_price,
            'max_price': max_price,
            'zip_code': zip_code,
            'venue': venue,
            'lon': lon,
            'lat': lat
        })
    cursor.close()
    return ret


if __name__ == '__main__':
    with urllib.request.urlopen("https://app.ticketmaster.com/discovery/v2/events.json?size=1&apikey=80Yiy3BkF0kupWGVzo75UtuPdt1Vu1V3&startDateTime=2017-12-09T00:12:00Z") as url:
        json = json.loads(url.read().decode())

    dataframe = extract_columns(json)
    dataframe
