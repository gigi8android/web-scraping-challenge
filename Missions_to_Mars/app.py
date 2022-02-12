
#################################################
# Import/ call dependencies and Setup
#################################################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#################################################
# Import file scrap_mars that contains all scrapping functions
#################################################
import scrape_mars


#################################################
# Create an instance of Flask, set static url path as coded in .html files
#################################################
app = Flask(__name__, static_url_path='', static_folder='')


#################################################
# Use PyMongo to establish Mongo connection for database mars_app
#################################################
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#################################################
# Route to render index.html template using data from MongoDB
#################################################
@app.route("/")
def home():

    # Find one lastest record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return the hompage/index page with mars_data (alias mars)
    return render_template("index.html", mars=mars_data)
#################################################


#################################################
# Route that triggers the scrape function
#################################################
@app.route("/scrape")
def scrape():

    # Execute all the scrape functions and get the returned data
    mars_data = scrape_mars.scrape()

    # Load the data that just had been scrapped to the database
    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)

    # Return to the homepage
    return redirect("/")
#################################################


#################################################
if __name__ == "__main__":
    app.run(debug=True)
