
# coding: utf-8

# In[208]:


import urllib.request, json 
import pandas as pd
import MySQLdb as mdb


# In[152]:


con = mdb.connect(host = 'localhost',
                  user = 'root', 
                  passwd = 'dwdstudent2015', 
                  charset='utf8', use_unicode=True);


# In[153]:


# Run a query to create a database that will hold the data
db_name = 'final_project'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)

# Create a database
cursor = con.cursor()
cursor.execute(create_db_query)
cursor.close()


# In[193]:


cursor = con.cursor()
table_name = 'events_bot'
create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table}
                                (title VARCHAR(100),
                                url VARCHAR(1000),
                                time VARCHAR(100),  
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



# In[199]:


def extract_columns(json):
    title = json['_embedded']['events'][0]['name']
    url = str(json['_embedded']['events'][0]['url'])
    time = json['_embedded']['events'][0]['dates']['start']['dateTime']
    category = json['_embedded']['events'][0]['classifications'][0]['segment']['name']
    min_price = str(json['_embedded']['events'][0]['priceRanges'][0]['min'])
    max_price = str(json['_embedded']['events'][0]['priceRanges'][0]['max'])
    zip_code = json['_embedded']['events'][0]['_embedded']['venues'][0]['postalCode']
    venue = json['_embedded']['events'][0]['_embedded']['venues'][0]['name']
    lon = json['_embedded']['events'][0]['_embedded']['venues'][0]['location']['longitude']
    lat = json['_embedded']['events'][0]['_embedded']['venues'][0]['location']['latitude']
    
    
    extracted_json = {
    'title': [title],
    'url': [str(url)],
    'time': time,
    'category': category,
    'min_price': min_price,
    'max_price': max_price,
    'zip_code': zip_code,
    'venue': venue,
    'lon': lon,
    'lat': lat
    }

    return extracted_json


# In[191]:


def store_data(json):
    
    dataframe = pd.DataFrame(extract_columns(json))
 
    query_template = '''INSERT INTO {db}.{table}(title,
                                            url, 
                                            time,
                                            category,
                                            min_price,
                                            max_price,
                                            zip_code,
                                            venue,
                                            lon,
                                            lat) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(db=db_name, table=table_name)
    cursor = con.cursor()

    for index, row in dataframe.iterrows():
        title = dataframe['title'][0]
        url = dataframe["url"][0]
        category = dataframe["category"][0]
        min_price = float(dataframe["min_price"])
        max_price = float(dataframe["max_price"])
        zip_code = dataframe['zip_code'][0]
        venue = dataframe['venue'][0]
        lon = dataframe['lon'][0]
        lat = dataframe['lat'][0]
        query_parameters = (title, url, time, category, min_price, max_price, zip_code, venue, lon, lat)
        cursor.execute(query_template, query_parameters)
    


        con.commit()
        cursor.close()
    


# In[209]:


#Example of Usage
if __name__ == '__main__':
    with urllib.request.urlopen("https://app.ticketmaster.com/discovery/v2/events.json?size=1&apikey=80Yiy3BkF0kupWGVzo75UtuPdt1Vu1V3&startDateTime=2017-12-09T00:12:00Z") as url:
        json = json.loads(url.read().decode())

    dataframe = extract_columns(json)
    dataframe



# In[ ]:




