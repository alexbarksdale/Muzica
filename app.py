from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import bcrypt

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_URI = os.environ.get('MONGO_URI')

client = MongoClient(f'{MONGO_URI}')
db = client.get_database('muzica_db')
listings = db.muzica_listings
users = db.muzica_users

app = Flask(__name__)
app.config['SECRET_KEY'] = f'{SECRET_KEY}'


@app.route('/')
def home_page():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    return render_template('home.html')


'''
Shows all of the listings from users using .find().
.find() looks through the entire mongo database.
'''
@app.route('/market')
def market_page():
    if 'username' in session:
        username = session['username']
        return render_template('market.html', listings=listings.find(), username=username)
    return render_template('market.html', listings=listings.find())


@app.route('/market/create')
def listing_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('create_listing.html', listing={}, title_type='Create Listing', type=' Create', username=username)


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
        'source': request.form.get('linksource'),
        'username': session['username']
    }

    while True:
        # Checks to see if ALL of the inputs have been filled. TODO: Fix
        print(listing)
        for i in listing:
            if listing[i].strip() == '':
                return render_template('create_listing.html', listing={}, type=' Create', title_type='Create Listing', noinput='You must enter all inputs')

        # Checks to see if the input contains numbers ONLY.
        if listing['price'].isdigit() or range(len(listing['price']) <= 0):
            listings_id = listings.insert_one(listing).inserted_id
            break
        else:
            return render_template('create_listing.html', error='Please input numbers only', listing={}, type=' Create', title_type='Create Listing')
    return redirect(url_for('market_page', listings_id=listings_id))


'''
Edit looks through the LISTINGS database and finds one ID corresponding to the
listing the user clicked.
'''
@app.route('/market/<listings_id>/edit')
def listing_edit(listings_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    listing = listings.find_one({'_id': ObjectId(listings_id)})

    if username != listing['username']:
        return redirect(url_for('market_page'))

    return render_template('edit_listing.html', title_type='Edit', title=listing['title'], type='Update', listing=listing, username=username)


'''
Updates the listing page with the edit, if any.
'''
@app.route('/market/<listings_id>', methods=['POST'])
def listing_update(listings_id):

    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    updated_listings = {
        'title': request.form.get('title'),
        'artist': request.form.get('artist'),
        'price': request.form.get('price'),
        'source': request.form.get('linksource')
    }
    # Checks to see if the input contains numbers ONLY.
    while True:
        if updated_listings['price'].isdigit() or range(len(updated_listings['price']) <= 0):
            listings.update_one(
                {'_id': ObjectId(listings_id)},
                {'$set': updated_listings})
            break
        else:
            return render_template('edit_listing.html', title_type='Edit', title=updated_listings['title'], type='Update', listing=updated_listings, username=username, error='Please input numbers only')

    return redirect(url_for('market_page', listings_id=listings_id))


@app.route('/market/<listings_id>/delete', methods=['POST'])
def listing_delete(listings_id):
    listings.delete_one({'_id': ObjectId(listings_id)})

    return redirect(url_for('market_page'))


'''
Acknowledgement: Learned how to make a login system from: @PrettyPrinted
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        login_user = users.find_one({'name': request.form['username']})
        invalid = 'Incorrect username or password'

        if login_user:
            # Takes in two parameters to compare passwords, takes password the user entered and takes the existing password
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('home_page'))
        return render_template('login.html', invalid=invalid)
    return render_template('login.html')


'''
Acknowledgement: Learned how to make a login system from: @PrettyPrinted
'''
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        existing_user = users.find_one({'name': request.form['username']})
        invalid_register = 'Username has already been taken'

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())

            users.insert(
                {'name': request.form['username'], 'password': hashpass})

            session['username'] = request.form['username']
            return redirect(url_for('home_page'))
        return render_template('register.html', invalid_register=invalid_register)
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
