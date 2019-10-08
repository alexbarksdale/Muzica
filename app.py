from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Muzica
listings = db.listings

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

'''
Shows all of the listings from users using .find().
.find() looks through the entire mongo database.
'''
@app.route('/market')
def market_page():
    return render_template('market.html', listings=listings.find())
    
@app.route('/market/create')
def listing_page():
    return render_template('create_listing.html')

'''
Submits a new listing after the user creates one.
RETURNS: redirected page back to all the listings.
'''
@app.route('/market', methods=['POST'])
def listing_submit():
    
    listing = {
        'title': request.form.get('title'),
        'artist': request.form.get('artist'),
        'price': request.form.get('price'),
        'source': request.form.get('linksource')
    }
    listings.insert_one(listing)
    return redirect(url_for('market_page'))
    
@app.route('/market/song/details')
def listing_details():
    return render_template('songdetails.html')
    