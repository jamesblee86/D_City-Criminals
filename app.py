#################################################
# Dependencies
#################################################

import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pymongo


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
# --------------------------------------------------
db = client.DenverCrime
coll = db.Population
crimeColl = db.Crime


@app.route("/")
def index():
    """Return the homepage """
    return render_template("index.html")


@app.route("/population")
def population():
    Denver_population = coll.find({"NAME": "Denver city"})

    print(Denver_population)

    pop_mongo_doc = Denver_population[0]

    return jsonify({
        "NAME": pop_mongo_doc["NAME"],
        "POPESTIMATE2014": pop_mongo_doc["POPESTIMATE2014"],
        "POPESTIMATE2015": pop_mongo_doc["POPESTIMATE2015"],
        "POPESTIMATE2016": pop_mongo_doc["POPESTIMATE2016"],
        "POPESTIMATE2017": pop_mongo_doc["POPESTIMATE2017"],
        "POPESTIMATE2018": pop_mongo_doc["POPESTIMATE2018"]
    })


@app.route("/crimes")
def crimes():
    sampleCrimesMurder = crimeColl.find({
        "OFFENSE_CATEGORY_ID":"murder",
    })

    murder_crimes_mongo_docs = [{
        "OFFENSE_CATEGORY_ID": murder_crimes_mongo_docs["OFFENSE_CATEGORY_ID"],
        "INCIDENT_ID": murder_crimes_mongo_docs['INCIDENT_ID'],
        "FIRST_OCCURRENCE_DATE": murder_crimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
        "GEO_LON": murder_crimes_mongo_docs["GEO_LON"],
        "GEO_LAT": murder_crimes_mongo_docs["GEO_LAT"]

    } for murder_crimes_mongo_docs in sampleCrimesMurder]

    sampleCrimesTrafficAccident = crimeColl.find({
        "OFFENSE_CATEGORY_ID":"traffic-accident",
    })

    traffic_accident_crimes_mongo_docs = [{
        "OFFENSE_CATEGORY_ID": traffic_accident_crimes_mongo_docs["OFFENSE_CATEGORY_ID"],
        "INCIDENT_ID": traffic_accident_crimes_mongo_docs['INCIDENT_ID'],
        "FIRST_OCCURRENCE_DATE": traffic_accident_crimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
        "GEO_LON": traffic_accident_crimes_mongo_docs["GEO_LON"],
        "GEO_LAT": traffic_accident_crimes_mongo_docs["GEO_LAT"]

    } for traffic_accident_crimes_mongo_docs in sampleCrimesTrafficAccident]

    sampleCrimesBurglary = crimeColl.find({
        "OFFENSE_CATEGORY_ID":"burglary",
    })

    burglary_crimes_mongo_docs = [{
        "OFFENSE_CATEGORY_ID": burglary_crimes_mongo_docs["OFFENSE_CATEGORY_ID"],
        "INCIDENT_ID": burglary_crimes_mongo_docs['INCIDENT_ID'],
        "FIRST_OCCURRENCE_DATE": burglary_crimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
        "GEO_LON": burglary_crimes_mongo_docs["GEO_LON"],
        "GEO_LAT": burglary_crimes_mongo_docs["GEO_LAT"]

    } for burglary_crimes_mongo_docs in sampleCrimesBurglary]

    sampleCrimesDrugAlcohol = crimeColl.find({
        "OFFENSE_CATEGORY_ID":"drug-alcohol",
    })

    drug_alcohol_crimes_mongo_docs = [{
        "OFFENSE_CATEGORY_ID": drug_alcohol_crimes_mongo_docs["OFFENSE_CATEGORY_ID"],
        "INCIDENT_ID": drug_alcohol_crimes_mongo_docs['INCIDENT_ID'],
        "FIRST_OCCURRENCE_DATE": drug_alcohol_crimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
        "GEO_LON": drug_alcohol_crimes_mongo_docs["GEO_LON"],
        "GEO_LAT": drug_alcohol_crimes_mongo_docs["GEO_LAT"]

    } for drug_alcohol_crimes_mongo_docs in sampleCrimesDrugAlcohol]

    sampleCrimesSexualAssault = crimeColl.find({
        "OFFENSE_CATEGORY_ID":"sexual-assault",
    })

    sexual_assault_crimes_mongo_docs = [{
        "OFFENSE_CATEGORY_ID": sexual_assault_crimes_mongo_docs["OFFENSE_CATEGORY_ID"],
        "INCIDENT_ID": sexual_assault_crimes_mongo_docs['INCIDENT_ID'],
        "FIRST_OCCURRENCE_DATE": sexual_assault_crimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
        "GEO_LON": sexual_assault_crimes_mongo_docs["GEO_LON"],
        "GEO_LAT": sexual_assault_crimes_mongo_docs["GEO_LAT"]

    } for sexual_assault_crimes_mongo_docs in sampleCrimesSexualAssault]

    sampleCrimesRobbery = crimeColl.find({
        "OFFENSE_CATEGORY_ID":"robbery",
    })

    robbery_crimes_mongo_docs = [{
        "OFFENSE_CATEGORY_ID": robbery_crimes_mongo_docs["OFFENSE_CATEGORY_ID"],
        "INCIDENT_ID": robbery_crimes_mongo_docs['INCIDENT_ID'],
        "FIRST_OCCURRENCE_DATE": robbery_crimes_mongo_docs["FIRST_OCCURRENCE_DATE"],
        "GEO_LON": robbery_crimes_mongo_docs["GEO_LON"],
        "GEO_LAT": robbery_crimes_mongo_docs["GEO_LAT"]

    } for robbery_crimes_mongo_docs in sampleCrimesRobbery]

    return jsonify(murder_crimes_mongo_docs,traffic_accident_crimes_mongo_docs,burglary_crimes_mongo_docs,burglary_crimes_mongo_docs,drug_alcohol_crimes_mongo_docs,sexual_assault_crimes_mongo_docs,robbery_crimes_mongo_docs)


if __name__ == "__main__":
    app.run(debug=True)