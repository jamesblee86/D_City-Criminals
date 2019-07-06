#################################################
# Dependencies
#################################################

import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pymongo
import json


#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn, ConnectTimeoutMS=30000)

# declare database
#--------------------------------------------------
db = client.DenverCrime
coll = db.Population
crimeColl = db.Crime

#  homepage
@app.route("/")
def index():
    """Return the homepage """
    return render_template("index.html")



# page for population results
@app.route("/population")
def population():
    Denver_population = coll.find({"NAME": "Denver city"})
    
    print(Denver_population)
   
    pop_mongo_doc = Denver_population[0]
    print(pop_mongo_doc)

    yearList = ["2014", "2015", "2016", "2017", "2018"]
    popList = [pop_mongo_doc["POPESTIMATE2014"],
                pop_mongo_doc["POPESTIMATE2015"],
                pop_mongo_doc["POPESTIMATE2016"],
                pop_mongo_doc["POPESTIMATE2017"],
                pop_mongo_doc["POPESTIMATE2018"]
                ]
    # print (yearList, popList)

    data = {"year":yearList, "population":popList}
    # 
    
    return jsonify(data)
   


# page for selected crimes
@app.route("/crimes/<crime>")
def crimes(crime):

# murder documents--------------------------------------------------------
# note: code was written when we were going to grab just murder crimes but then
# we changed the route/collection find to pick any crime - we decided not to 
# revise the code below that appears to look for only murders

    sampleCrimesMurder = crimeColl.find({
        "OFFENSE_CATEGORY_ID":crime
         })
    

    murderCrimes_mongo_docs = sampleCrimesMurder

    murder_df = pd.DataFrame([{
            "OFFENSE_CATEGORY_ID": murderCrimes_mongo_docs["OFFENSE_CATEGORY_ID"],
            "FIRST_OCCURRENCE_DATE": murderCrimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
            "GEO_LON": murderCrimes_mongo_docs["GEO_LON"],
            "GEO_LAT": murderCrimes_mongo_docs["GEO_LAT"]

    } for murderCrimes_mongo_docs in sampleCrimesMurder])
    
    murder_df['DATE_YEAR_MONTH'] = pd.to_datetime(murder_df.FIRST_OCCURRENCE_DATE).dt.to_period('Y') 
    murder_df['DATE_YEAR'] = pd.to_datetime(murder_df.FIRST_OCCURRENCE_DATE).dt.year

    murder_df = murder_df.loc[murder_df['DATE_YEAR']<2019]
    murder_by_month = murder_df.groupby('DATE_YEAR').count()['OFFENSE_CATEGORY_ID']
   
    return jsonify({
        "year_month": murder_by_month.index.tolist(),
        "count_murders" : murder_by_month.tolist()
    })
    
    

if __name__ == "__main__":
    app.run(debug=True)
