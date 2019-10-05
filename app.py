from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')
    

@app.route('/market')
def market_page():
    return render_template('market.html')
    
@app.route('/create')
def login_page():
    return render_template('create_listing.html')