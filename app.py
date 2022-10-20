from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection - connect app to Mongo database 'mars_app'
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Defining the route for the HTML page
@app.route("/")
# Link the web app (visual) to the code
def index():
   # Find the "mars" collection in the database
   mars = mongo.db.mars.find_one()
   # Display the scraped content using index.html file as the HTML template and the 'mars' collection in MongoDB
   return render_template("index.html", mars=mars)


# Setting up the scraping route (a button will scrape the data)
@app.route("/scrape")
def scrape():
   # Access to the 'Mars' collection in the database
   mars = mongo.db.mars
   # Hold the newly scraped data using scraping.py script
   mars_data = scraping.scrape_all()
   # Using data in mars_data, insert data if an identical record does not already exist
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # Navigate page back to / to see updated content
   return redirect('/', code=302)
   

# Telling Flask to run
if __name__ == "__main__":
   app.run()
