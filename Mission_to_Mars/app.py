###Homework app
from flask import Flask, render_template, redirect, Markup
from flask_table import Table, Col
from flask_pymongo import PyMongo
import scrape_mars
import numpy as np
import pandas as pd

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    d_data = mongo.db.collection.find_one()
    table_markup = Markup(d_data["table"])
    # Return template and data
    
    return render_template("index.html", vacation=d_data, table_info=table_markup)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
    resy = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, resy, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
