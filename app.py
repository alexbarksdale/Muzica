from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Muzica
listings = db.listings

app = Flask(__name__)

@app.route('/')
def home_page():
    # RETURNS homepage
    return render_template('home.html')

@app.route('/market')
def market_page():
    return render_template('market.html', listings=listings.find())
    
@app.route('/market/create')
def listing_page():
    return render_template('create_listing.html')
    
@app.route('/market', methods=['POST'])
def listing_submit():
    
    # SUBMIT a new listing
    listing = {
        'title': request.form.get('title'),
        'artist': request.form.get('artist'),
        'price': request.form.get('price'),
        'source': request.form.get('linksource')
    }
    listings.insert_one(listing)
    return redirect(url_for('market_page'))
    