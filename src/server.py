# Decide wheter to use SQLAlchemy (ORM) or MySQLdb (Might have to use a fork, MySQLDb does not have good python3 support) 
# Please follow the following naming convention: long_function_name(var_one,var_two)
from flask import Flask,flash,session, render_template, request, redirect, Response ,jsonify, json, url_for

app = Flask(__name__)

@app.route('/')
def index():
    '''This function renders the index page of the EventManagement site'''
    return render_template('index.html')

@app.route('/doregister',methods = ['POST'])
def do_register():
    '''This function enters user details into the database, then shows the "You have registered! page'''
    #Add actual functionality here. Ideally have another py file that handles all user related interactions, import and call functions here
    # Using the redirect function because then the "/registered endpoint will show up, which makes more sense to user"
    return redirect(url_for('registered'))

@app.route('/register')
def register():
    '''This function renders the register page'''
    return render_template('register.html')

@app.route('/registered')
def registered():
    return render_template('registered.html')


@app.route('/dosignin',methods=['POST'])
def do_sigin():
    '''This function authenticates the sign in by checking password against database.
    It also creates a session, with the Username stored.
    Redirects to /home so that it makes more sense to user'''
    #add checking procedure
    #dynamically add error message in signin in case validation fails
    #in case of sucesss add session variables 
    return redirect(url_for('home'))

@app.route('/home')
def home():
    '''This funnction shows the user the homepage. Username will be displayed top left, 
    and all current events will be displayed on the page, dynamically.'''
    # use render templeate functionality to automatically add name and other data 
    return render_template('manage_events.html')

if __name__ == '__main__':
	# run!
	app.run(debug=True)
