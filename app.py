from flask import app, flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set up flask
# app = flask (__name__)

#Use flask_pymongo to set up a mongo connection
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#route to html page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

#set up scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upset=True)
    return redirect('/', code=302)

# have the code run
if __name__ == '__main__':
    app.run()
    
#