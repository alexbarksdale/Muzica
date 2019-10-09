from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import bcrypt

MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(f'{MONGO_URI}')

db = client.get_database('muzica_db')
listings = db.muzica_listings

app = Flask(__name__)


@app.route('/')
def home_page():

    if 'username' in session:
        return 'You are logged in as ' + session['username']

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
    return render_template('create_listing.html', listing={}, title_type='Create Listing', type='Create')


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

    listings_id = listings.insert_one(listing).inserted_id
    return redirect(url_for('market_page', listings_id=listings_id))


'''
Edit looks through the LISTINGS database and finds one ID corresponding to the
listing the user clicked.
'''


@app.route('/market/<listings_id>/edit')
def listing_edit(listings_id):
    listing = listings.find_one({'_id': ObjectId(listings_id)})
    return render_template('edit_listing.html', title_type='Edit', title=listing['title'], type='Update', listing=listing)


'''
Updates the listing page with the edit, if any.
'''


@app.route('/market/<listings_id>', methods=['POST'])
def listing_update(listings_id):
    updated_listings = {
        'title': request.form.get('title'),
        'artist': request.form.get('artist'),
        'price': request.form.get('price'),
        'source': request.form.get('linksource')
    }

    listings.update_one(
        {'_id': ObjectId(listings_id)},
        {'$set': updated_listings})

    return redirect(url_for('market_page', listings_id=listings_id))


@app.route('/market/<listings_id>/delete', methods=['POST'])
def listing_delete(listings_id):
    listings.delete_one({'_id': ObjectId(listings_id)})
    return redirect(url_for('market_page'))


# TEST

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = client.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())

            users.insert(
                {'name': request.form['username'], 'password': hashpass})

            session['username'] = request.form['username']
            return redirect(url_for('home_page'))

        return 'That username already exists!'

    return render_template('register.html')
