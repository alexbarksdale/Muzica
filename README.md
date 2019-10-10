# Muzica

![Muzica](https://i.imgur.com/bOMBDtP.png)

## About
Muzica allows users to sell music through a market listing. Each listing is unique to the user's account which allows
them to edit their listings only, if needed.

**[Visit here](https://muzica-ab.herokuapp.com/) to see the live version on Heroku.**

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
If you haven't already installed pip3 for Python3
```
sudo apt install python3-pip
```

### Installing

1. Clone the respository
```
git clone https://github.com/alexbarksdale/Muzica.git
```
2. Make sure you're in the correct directory

3. You now need to create a virtual environment for the project. Open your termianl and run:
```
python3 -m venv env
```
4. Now that you have a virtual environment for the project you need to activate it, type the following in the console:
```
source env/bin/activate
```
Note: You shouldn't see anythng happen!

5. Now to quickly install everything you need, type the following in the console:
```
pip3 install -r requirements.txt
```
This will install everything required in my requirements.txt

----------------------------------------------------------------
## IMPORTANT
I used MongoDB Atlas as the database so you will need to create one in order to run this on your machine or [visit here](https://muzica-ab.herokuapp.com/) to see the live version on Heroku.

### MongoDB Atlas Setup
1. Before setting up your Atlas, create '.env' file in your text editor
2. Create an account [here](https://www.mongodb.com/cloud/atlas)
3. Once you're signed in you should be brought to the dashboard
4. Build a new cluster for your database
5. Locate the 'connect' button, you should be prompted with a 'Connect to (ClusterName)'
6. Click 'Connect Your Application' and select 'Python' as the driver and the version of your python
7. Copy the 'Connection String Only' and it should look something like 
```
mongodb+srv://(YOUR_USERNAME):<password>@(CLUSTER_NAME)-(LOTS_OF_TEXT)
```
8. Go to your .env file and type the following:
```
MONGODB_URI=(YOUR_CONNECTION_STRING)
SECRET_KEY=(ANYTHING YOU WANT)
```
9. In app.py scroll to the very top and make sure everything below is UNCOMMENTED out:
```
'#! ------------ Comment out when pushing to HEROKU ------------' 
```
10. Make sure below the following is COMMENTED out: 
```
#! ------------ Comment out when using LOCALHOST ------------
```

----------------------------------------------------------------
COMPLETE 'IMPORTANT' before running!

6. Open your terminal and run flask
```
export FLASK_ENV=development; flask run
```
You should see something similar to the output below:
```
 * Environment: development
 * Debug mode: on
 * Running on http://(YOUR_LOCAL_HOST)/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: (PIN)
```
### Running Tests
1. To simply run the test functions, type the following in your terminal
```
python3 test_app.py
```
## Built With

* [Flask](https://palletsprojects.com/p/flask/) - Lightweight web application framework
* [Jinja](https://palletsprojects.com/p/jinja/) - Template engine for python
* [Heroku](https://www.heroku.com/) - Runs Muzica in the cloud. [Visit here](https://muzica-ab.herokuapp.com/) to see the live version on Heroku.

## Acknowledgments

* Learned how to make a login system from @PrettyPrinted

